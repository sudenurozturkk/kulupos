"""KulüpOS HTTP API + static UI. Binds to localhost only."""
from __future__ import annotations

import asyncio
import contextlib
import hashlib
import json
import os
import re
import sqlite3
from datetime import date, timedelta
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from . import analysis, analyzer, assistant, auth, coach, db, units as unitmod, export, insights, llm, meetings, people, report, seed
from .parser import MAX_BYTES, parse_report, read_export

ROOT = Path(__file__).resolve().parent.parent
DEMOS = {
    "tr": ("FUB3V Yönetim 2026", ROOT / "demo" / "kbk-yonetim-tr.txt",
           ["Yönetim", "Etkinlik", "Sosyal Medya", "Sponsorluk", "Teknik"]),
    "en": ("Robotics Club Board", ROOT / "demo" / "robotics-club-en.txt",
           ["Board", "Events", "Social Media", "Sponsorship", "Tech"]),
}

@contextlib.asynccontextmanager
async def lifespan(_: FastAPI):
    db.recover_stale_analyses()
    yield


app = FastAPI(title="KulüpOS", docs_url="/api/docs", lifespan=lifespan)
_tasks: set[asyncio.Task] = set()


@app.middleware("http")
async def require_sign_in(request: Request, call_next):
    """Every API call except sign-in itself and the health check needs a valid session (unless PANO_AUTH=0)."""
    path = request.url.path
    if auth.enabled() and path.startswith("/api/") and not path.startswith(auth.OPEN)             and not auth.user_of(request.cookies.get(auth.COOKIE)):
        return JSONResponse({"detail": "Giriş gerekli / sign-in required"}, status_code=401)
    m = re.match(r"/api/chats/(\d+)", path)
    if auth.enabled() and m and auth.is_guest(request.cookies.get(auth.COOKIE)):  # demo visitors see the sample club only
        row = db._rows("SELECT is_sample FROM chats WHERE id = ?", (int(m.group(1)),))
        if row and not row[0]["is_sample"]:
            return JSONResponse({"detail": "Demo oturumu yalnızca örnek kulübü görür / demo session sees the sample club only"}, status_code=403)
    return await call_next(request)


class Credentials(BaseModel):
    username: str
    password: str


def _session_response(token: str, username: str) -> JSONResponse:
    r = JSONResponse({"user": username})
    r.set_cookie(auth.COOKIE, token, httponly=True, samesite="lax", max_age=60 * 60 * 24 * 7)
    return r


@app.post("/api/auth/guest")
def auth_guest():
    return _session_response(auth.guest(), auth.GUEST)


@app.get("/api/auth/me")
def auth_me(request: Request):
    user = auth.user_of(request.cookies.get(auth.COOKIE))
    return {"user": user, "auth": auth.enabled(), "guest": auth.is_guest(request.cookies.get(auth.COOKIE))}


@app.post("/api/auth/register")
def auth_register(body: Credentials):
    try:
        return _session_response(auth.register(body.username, body.password), body.username.strip())
    except ValueError as e:
        raise HTTPException(400, str(e))
    except PermissionError as e:
        raise HTTPException(403, str(e))


@app.post("/api/auth/login")
def auth_login(body: Credentials):
    try:
        return _session_response(auth.login(body.username, body.password), body.username.strip())
    except PermissionError as e:
        raise HTTPException(401, str(e))


@app.post("/api/auth/logout")
def auth_logout(request: Request):
    auth.logout(request.cookies.get(auth.COOKIE))
    r = JSONResponse({"ok": True})
    r.delete_cookie(auth.COOKIE)
    return r


def today() -> date:
    override = os.environ.get("PANO_TODAY")
    return date.fromisoformat(override) if override else date.today()


def _chat_or_404(chat_id: int) -> dict:
    chat = db.get_chat(chat_id)
    if not chat:
        raise HTTPException(404, "chat not found")
    return chat


def _name_from_filename(filename: str) -> str:
    stem = Path(filename).stem
    stem = re.sub(r"^(WhatsApp\s+(Chat\s+with|Sohbeti\s*-?)\s*|_chat$)", "", stem, flags=re.I).strip(" -_")
    return stem or "WhatsApp"


def _read(data: bytes):
    """Validate an upload; returns (messages, skipped_lines). Raises HTTPException(400/413)."""
    if not data:
        raise HTTPException(400, "Dosya boş / the file is empty")
    if len(data) > MAX_BYTES:
        raise HTTPException(413, "Dosya 5 MB sınırını aşıyor / file exceeds the 5 MB limit")
    try:
        messages, skipped = parse_report(read_export(data))
    except Exception as e:
        raise HTTPException(400, f"Dosya okunamadı / could not read file: {e}")
    if not any(m.sender for m in messages):
        raise HTTPException(400, "Bu bir WhatsApp sohbet dışa aktarımı gibi görünmüyor / "
                                 "this does not look like a WhatsApp export")
    return messages, skipped


def _import(data: bytes, name: str, units: list[str], source_name: str | None = None) -> dict:
    messages, _ = _read(data)
    chat_id = db.create_chat(name, units, messages, hashlib.sha256(data).hexdigest(), source_name)
    return db.get_chat(chat_id)


def _start_analysis(chat_id: int) -> None:
    if analyzer.progress(chat_id).get("state") in ("queued", "running"):
        return
    # Mark it queued now: the task only starts later, and a second click must not start another run.
    analyzer.PROGRESS[chat_id] = {"state": "queued", "done": 0, "total": 0, "found": [],
                                  "started": 0, "error": None}
    task = asyncio.create_task(analyzer.analyze(chat_id))
    _tasks.add(task)
    task.add_done_callback(_tasks.discard)


# ---- routes ----------------------------------------------------------------

@app.get("/api/health")
async def health():
    return await llm.health()


@app.get("/api/chats")
def chats(request: Request):
    rows = db.list_chats()
    return [c for c in rows if c["is_sample"]] if auth.enabled() and auth.is_guest(request.cookies.get(auth.COOKIE)) else rows


@app.post("/api/chats")
async def upload(request: Request, filename: str = "chat.txt", name: str = "", units: str = ""):
    data = await request.body()
    unit_list = [u.strip() for u in units.split(",") if u.strip()]
    return _import(data, name.strip() or _name_from_filename(filename), unit_list, filename)


@app.post("/api/preview")
async def preview(request: Request):
    """What an upload would import, without saving anything."""
    data = await request.body()
    messages, skipped = _read(data)
    real = [m for m in messages if m.sender]
    return {
        "messages": len(messages),
        "first_ts": messages[0].ts.isoformat(timespec="minutes"),
        "last_ts": messages[-1].ts.isoformat(timespec="minutes"),
        "senders": sorted({m.sender for m in real}),
        "skipped_lines": skipped,
        "duplicate_of": db.find_by_hash(hashlib.sha256(data).hexdigest()),
    }


@app.post("/api/seed")
def seed_sample():
    """First run: an empty database gets the fake sample club. No-op once chats exist or the sample was cleared."""
    chat_id = seed.seed_sample(today())
    return {"created": chat_id is not None, "chat_id": chat_id}


@app.delete("/api/sample")
def clear_sample():
    return {"removed": seed.clear_sample()}


SEED_TIMEOUT = float(os.environ.get("PANO_SEED_TIMEOUT", "5"))


@app.post("/api/demo/{lang}")
async def demo(lang: str):
    """tr: the filled sample club, opened instantly (no model, no analysis). en: the raw demo chat, analysed in the background."""
    if lang not in DEMOS:
        raise HTTPException(404)
    if lang == "tr":
        try:
            chat_id = await asyncio.wait_for(asyncio.to_thread(seed.ensure_sample, today()), SEED_TIMEOUT)
        except asyncio.TimeoutError:
            raise HTTPException(504, f"Demo {SEED_TIMEOUT:g} saniyede açılamadı; veritabanı meşgul olabilir. Başka bir KulüpOS "
                                     "penceresi/süreci açıksa kapatıp tekrar deneyin / the demo did not open in time; "
                                     "the database may be busy, close any other KulüpOS process and retry")
        except sqlite3.Error as e:
            raise HTTPException(503, f"Veritabanı hatası / database error: {type(e).__name__}")
        return db.get_chat(chat_id)
    name, path, units = DEMOS[lang]
    for c in db.list_chats():  # reuse an already analysed demo: instant on stage
        if c["name"] == name and c["status"] in ("ready", "analyzing"):
            return db.get_chat(c["id"])
    return _import(path.read_bytes(), name, units)


@app.post("/api/chats/{chat_id}/import")
async def reimport(chat_id: int, request: Request):
    """Upload a newer export of the same group: only new messages are added and analysed."""
    _chat_or_404(chat_id)
    added = db.append_messages(chat_id, _read(await request.body())[0])
    if added:
        _start_analysis(chat_id)
    return {"added": added}


class ChatPatch(BaseModel):
    name: str | None = None
    units: list[str] | None = None          # the full committee list after the change
    renames: dict[str, str] | None = None   # {old name: new name}, applied before `units`
    unit_members: dict[str, str] | None = None  # {committee: "Ad Soyad, Ad Soyad"}: free text, comma separated


@app.patch("/api/chats/{chat_id}")
def patch_chat(chat_id: int, body: ChatPatch):
    chat = _chat_or_404(chat_id)
    if body.name is not None:
        if not body.name.strip():
            raise HTTPException(400, "Ad boş olamaz / name cannot be empty")
        db.update_chat(chat_id, name=body.name.strip())
    if body.units is not None or body.renames:
        renames = {o: n.strip() for o, n in (body.renames or {}).items()}
        if any(o not in chat["units"] or not n for o, n in renames.items()):
            raise HTTPException(400, "Komite bulunamadı veya ad boş / unknown committee or empty name")
        after_renames = [renames.get(u, u) for u in chat["units"]]
        final = [u.strip() for u in (body.units if body.units is not None else after_renames)]
        if any(not u for u in final) or len({u.casefold() for u in final}) != len(final):
            raise HTTPException(400, "Komite adları boş veya tekrar olamaz / names must be unique and non-empty")
        db.set_units(chat_id, final, renames)
    if body.unit_members is not None:
        units = db.get_chat(chat_id)["units"]
        if any(u not in units for u in body.unit_members):
            raise HTTPException(400, "Komite bulunamadı / unknown committee")
        cleaned = {u: ", ".join(n for n in (" ".join(x.split()) for x in v.split(",")) if n) for u, v in body.unit_members.items()}
        merged = {**db.get_chat(chat_id)["unit_members"], **cleaned}  # only the sent committees change
        db.update_chat(chat_id, unit_members={u: v for u, v in merged.items() if v})
    return db.get_chat(chat_id)


@app.delete("/api/chats/{chat_id}")
def delete_chat(chat_id: int):
    db.delete_chat(chat_id)
    return {"ok": True}


@app.post("/api/chats/{chat_id}/analyze")
async def analyze(chat_id: int, reset: bool = False):
    _chat_or_404(chat_id)
    if reset and analyzer.progress(chat_id).get("state") not in ("queued", "running"):
        db.reset_analysis(chat_id)
    _start_analysis(chat_id)
    return analyzer.progress(chat_id)


@app.get("/api/chats/{chat_id}/progress")
def progress(chat_id: int):
    return analyzer.progress(chat_id)


def _with_source(chat_id: int, rows: list[dict]) -> list[dict]:
    """Attach the source message (sender, time, shortened text) so the review cards can quote it."""
    for r in rows:
        idx = r.get("source_idx")
        m = db.get_messages(chat_id, idx, idx) if idx is not None else []
        r["source"] = {"sender": m[0]["sender"], "ts": m[0]["ts"], "text": m[0]["text"][:280]} if m else None
        if r.get("meeting_id") and r.get("source_text"):  # a note line, not a chat message: no sender, no time
            title = (db.get_meeting(r["meeting_id"]) or {}).get("title")
            r["source"] = {"sender": None, "ts": None, "text": r["source_text"], "meeting_id": r["meeting_id"],
                           "meeting_title": title}
    return rows


@app.get("/api/chats/{chat_id}/board")
def board(chat_id: int):
    chat = _chat_or_404(chat_id)
    items = db.get_items(chat_id)
    t = today()
    soon = (t + timedelta(days=3)).isoformat()
    tasks = [i for i in items if i["kind"] == "task"]
    open_tasks = [i for i in tasks if i["status"] == "open"]
    missed = {
        "questions": [i for i in items if i["kind"] == "question" and i["status"] == "open"],
        "orphans": [i for i in open_tasks if not i["owner"]],
        "overdue": [i for i in open_tasks if i["due"] and i["due"] < t.isoformat()],
        "soon": [i for i in open_tasks if i["due"] and t.isoformat() <= i["due"] <= soon],
        **coach.overlooked(chat_id, t),
    }
    return {
        "chat": chat,
        "today": t.isoformat(),
        "members": db.senders(chat_id),
        "tasks": tasks,
        "questions": [i for i in items if i["kind"] == "question"],
        "decisions": [i for i in items if i["kind"] == "decision"],
        "events": sorted((i for i in items if i["kind"] == "event"), key=lambda e: e["due"] or ""),
        "missed": missed,
        "review": _with_source(chat_id, db.get_items(chat_id, review="proposed")),  # AI suggestions awaiting approval
        "changes": _with_source(chat_id, db.get_changes(chat_id)),  # AI edits to approved items awaiting approval
        "review_total": len(db.get_items(chat_id, review="proposed")) + len(db.get_changes(chat_id)),
        "event_compare": analysis.compare(items, t.isoformat()),
        "overview": insights.overview(chat, items, db.senders(chat_id), t),
        "meetings": meetings.panel_cards(db.get_meetings(chat_id), items, t.isoformat()),
        "progress": analyzer.progress(chat_id),
    }


class PlanReq(BaseModel):
    goal: str


@app.post("/api/chats/{chat_id}/plan")
async def plan(chat_id: int, body: PlanReq):
    _chat_or_404(chat_id)
    try:
        return await insights.plan_event(chat_id, body.goal, today())
    except llm.LLMError as e:
        raise HTTPException(503, str(e))


@app.post("/api/chats/{chat_id}/ideas")
async def event_ideas(chat_id: int):
    """Slow (local model): new event ideas grounded in the club's held events."""
    _chat_or_404(chat_id)
    try:
        return await insights.suggest_events(chat_id, today())
    except llm.LLMError as e:
        raise HTTPException(503, str(e))


@app.get("/api/chats/{chat_id}/saved/{kind}")
def saved_ai(chat_id: int, kind: str):
    """Event ideas / plans the model produced earlier; they stay until deleted."""
    _chat_or_404(chat_id)
    if kind not in ("ideas", "plan", "week", "handover", "recap"):
        raise HTTPException(404, "unknown kind")
    return {"saved": db.list_ai(chat_id, kind)}


@app.post("/api/chats/{chat_id}/week")
async def week_plan(chat_id: int):
    """Slow (local model): the next 7 days in order, each step tied to a recorded item or team."""
    _chat_or_404(chat_id)
    try:
        return await coach.week_plan(chat_id, today())
    except llm.LLMError as e:
        raise HTTPException(503, str(e))


@app.get("/api/chats/{chat_id}/weekly-report", response_class=HTMLResponse)
def weekly_report(chat_id: int):
    """Printable one-page weekly report (browser: save as PDF): figures from the records + the saved Gemma roadmap."""
    _chat_or_404(chat_id)
    return coach.weekly_html(chat_id, today())


@app.post("/api/chats/{chat_id}/handover")
async def handover(chat_id: int):
    """Slow (local model): handover report for the next board, written from the records only."""
    _chat_or_404(chat_id)
    try:
        return await coach.handover(chat_id, today())
    except llm.LLMError as e:
        raise HTTPException(503, str(e))
    except report.ReportRejected as e:
        raise HTTPException(422, {"message": "Rapor, kayıtlı veride olmayan sayı veya isim içerdiği için reddedildi / "
                                             "rejected: it contained figures or names that are not in the data",
                                  "unsupported": e.unsupported})


@app.delete("/api/saved/{saved_id}")
def delete_saved_ai(saved_id: int):
    db.delete_ai(saved_id)
    return {"ok": True}


class PlanAccept(BaseModel):
    event_title: str | None = None
    event_date: str | None = None
    tasks: list[dict]
    meetings: list[dict] = []


@app.post("/api/chats/{chat_id}/plan/accept")
def plan_accept(chat_id: int, body: PlanAccept):
    """Only the tasks the user ticked are written to the board."""
    _chat_or_404(chat_id)
    for t in body.tasks:
        item_id = db.add_item(chat_id, "task", title=t.get("title", "").strip() or "?", owner=t.get("owner") or None,
                              due=t.get("due") or None, unit=t.get("unit") or None)
        db.update_item(item_id, user=True)
    if body.event_title and body.event_date:
        item_id = db.add_item(chat_id, "event", title=body.event_title, due=body.event_date)
        db.update_item(item_id, user=True)
    for m in body.meetings:  # ticked preparation meetings become planned meetings
        db.add_meeting(chat_id, title=(m.get("title") or "?").strip(), date=meetings.valid_date(m.get("date")),
                       units=m.get("units") or [], agenda=m.get("agenda") or None, status="planned")
    return {"added": len(body.tasks), "meetings": len(body.meetings)}


@app.get("/api/chats/{chat_id}/export.md", response_class=PlainTextResponse)
def export_md(chat_id: int):
    """The whole board as Markdown, with source references, for Notion/GitHub/Docs."""
    b = board(chat_id)
    out = [f"# {b['chat']['name']}", "", f"_KulüpOS · {b['today']}_", "", "## Tasks", ""]
    for unit in [*b["chat"]["units"], None]:
        rows = [t for t in b["tasks"] if (t["unit"] or None) == unit]
        if not rows:
            continue
        out.append(f"### {unit or '—'}")
        for t in rows:
            meta = ", ".join(filter(None, [t["owner"], t["due"], f"msg #{t['source_idx']}" if t["source_idx"] is not None else ""]))
            out.append(f"- [{'x' if t['status'] == 'done' else ' '}] {t['title']}" + (f" ({meta})" if meta else ""))
        out.append("")
    for title, key in (("Open questions", "questions"), ("Decisions", "decisions"), ("Events", "events")):
        rows = b[key] if key != "questions" else [q for q in b[key] if q["status"] == "open"]
        if rows:
            out += [f"## {title}", ""] + [
                f"- {r['title']}" + (f" — {r['due']}" if r["due"] else "") + (f" {r['time']}" if r["time"] else "")
                for r in rows] + [""]
    return "\n".join(out)


@app.get("/api/chats/{chat_id}/export")
def export_file(chat_id: int, what: str = "tasks", format: str = "csv", status: str | None = None,
                owner: str | None = None, unit: str | None = None, date_from: str | None = None,
                date_to: str | None = None):
    """what = tasks | decisions | questions | summary; format = csv | json (summary is always Markdown)."""
    chat = _chat_or_404(chat_id)
    t = today().isoformat()
    try:
        if what == "summary":
            body, ext, mime = export.summary_md(chat_id, status, owner, unit, date_from, date_to, t), "md", "text/markdown"
        else:
            rows, filters = export.rows_for(chat_id, what, status, owner, unit, date_from, date_to)
            if format == "json":
                body, ext, mime = export.to_json(rows, filters, t), "json", "application/json"
            elif format == "csv":
                body, ext, mime = export.to_csv(rows, filters, t), "csv", "text/csv"
            else:
                raise export.FilterError("format: csv | json")
    except export.FilterError as e:
        raise HTTPException(400, str(e))
    name = re.sub(r"[^A-Za-z0-9._-]+", "_", f"{chat['name']}-{what}")
    return Response(body, media_type=f"{mime}; charset=utf-8",
                    headers={"Content-Disposition": f'attachment; filename="{name}.{ext}"'})


@app.get("/api/chats/{chat_id}/messages")
def messages(chat_id: int, around: int, radius: int = 4):
    _chat_or_404(chat_id)
    return db.get_messages(chat_id, max(0, around - radius), around + radius)


PHASES = ("idea", "planning", "confirmed", "held", "cancelled")
NUMERIC = ("attendees_expected", "attendees_actual", "budget_est", "budget_actual", "applications")
EVENT_ONLY = ("phase", "event_type", "event_units", "feedback_score", "feedback_note", "feedback_good", "feedback_bad",
              "feedback_comments", *NUMERIC)
FEEDBACK_LIMITS = {"feedback_note": 500, "feedback_good": 2000, "feedback_bad": 2000, "feedback_comments": 8000}


class EventFields(BaseModel):
    time: str | None = None
    place: str | None = None
    event_type: str | None = None
    phase: str | None = None
    event_units: list[str] | None = None
    attendees_expected: int | None = None
    attendees_actual: int | None = None
    budget_est: float | None = None
    budget_actual: float | None = None
    applications: int | None = None
    feedback_score: float | None = None  # 1-5, optional
    feedback_note: str | None = None
    feedback_good: str | None = None      # typed by the club: what went well / what fell short
    feedback_bad: str | None = None
    feedback_comments: str | None = None  # pasted participant comments, one per line
    notes: str | None = None
    event_id: int | None = None  # link a task/decision to an event


def _clean_event_fields(chat_id: int, fields: dict) -> dict:
    """Blank strings clear a field; numbers must be >= 0; links must point at an event of this chat."""
    for k, v in list(fields.items()):
        if isinstance(v, str):
            fields[k] = v.strip() or None
    if fields.get("phase") not in (None, *PHASES):
        raise HTTPException(400, "bad phase")
    for k in NUMERIC:
        if fields.get(k) is not None and fields[k] < 0:
            raise HTTPException(400, f"{k} must be >= 0")
    if fields.get("feedback_score") is not None and not 1 <= fields["feedback_score"] <= 5:
        raise HTTPException(400, "feedback_score must be between 1 and 5")
    for k, limit in FEEDBACK_LIMITS.items():
        if fields.get(k) and len(fields[k]) > limit:
            raise HTTPException(413, f"{k}: en fazla {limit} karakter / at most {limit} characters")
    if fields.get("event_id") is not None:
        ev = db.get_item(fields["event_id"])
        if not ev or ev["kind"] != "event" or ev["chat_id"] != chat_id:
            raise HTTPException(400, "event_id must be an event of this chat")
    if "event_units" in fields:
        fields["event_units"] = [u.strip() for u in (fields["event_units"] or []) if u.strip()]
    return fields


class ItemPatch(EventFields):
    title: str | None = None
    owner: str | None = None
    due: str | None = None
    unit: str | None = None
    status: str | None = None
    review: str | None = None  # approved | rejected
    validity: str | None = None  # decisions only: valid | changed | cancelled
    note: str | None = None    # why the status changed; goes to the item's history, not onto the item


STATUSES = {"question": ("open", "answered", "resolved", "invalid")}   # other kinds: open | done | answered


@app.get("/api/items/{item_id}/history")
def item_history(item_id: int):
    if not db.get_item(item_id):
        raise HTTPException(404)
    return db.get_history(item_id)


@app.patch("/api/items/{item_id}")
def patch_item(item_id: int, body: ItemPatch):
    if not db.get_item(item_id):
        raise HTTPException(404)
    # "" clears a field; omitted fields stay untouched.
    cur = db.get_item(item_id)
    fields = {k: (None if v == "" else v) for k, v in body.model_dump(exclude_unset=True).items()}
    note = fields.pop("note", None)
    fields = _clean_event_fields(cur["chat_id"], fields)
    if cur["kind"] != "event" and any(k in fields for k in EVENT_ONLY):
        raise HTTPException(400, "event fields only apply to events")
    if fields.get("event_id") == item_id:
        raise HTTPException(400, "an event cannot link to itself")
    for required in ("title", "status"):
        if fields.get(required, "") is None:
            del fields[required]
    if fields.get("status") not in (None, *STATUSES.get(cur["kind"], ("open", "done", "answered"))):
        raise HTTPException(400, "bad status")
    if fields.get("validity") not in (None, *db.VALIDITY):
        raise HTTPException(400, "bad validity")
    if fields.get("validity") and cur["kind"] != "decision":
        raise HTTPException(400, "validity only applies to decisions")
    if fields.get("review") not in (None, "approved", "rejected"):
        raise HTTPException(400, "bad review")
    if fields.get("review") is None:
        fields.pop("review", None)
    if fields.get("review") == "approved" and cur["needs_review"]:
        # no source -> never approvable; unclear date -> only after the user edited it
        if cur["needs_review"] == 1 or not (cur["user_edited"] or len(fields) > 1):
            raise HTTPException(409, "Kaynak bulunamadı / date unclear: düzenle veya reddet / edit or reject")
    # Approving/rejecting is a decision, not a correction: only real edits lock the item against the AI.
    db.update_item(item_id, user=any(k != "review" for k in fields), **fields)
    if cur["kind"] == "question" and fields.get("status") not in (None, cur["status"]):
        db.add_history(item_id, "status", cur["status"], fields["status"], note)
    if cur["kind"] == "decision":
        for f in ("validity", "title"):
            if fields.get(f) not in (None, cur[f]):
                db.add_history(item_id, f, cur[f], fields[f], note)
    return db.get_item(item_id)


class ChangeDecision(BaseModel):
    review: str  # approved | rejected


@app.patch("/api/changes/{change_id}")
def decide_change(change_id: int, body: ChangeDecision):
    ch = db.get_change(change_id)
    if not ch:
        raise HTTPException(404)
    if body.review not in ("approved", "rejected") or ch["review"] != "proposed":
        raise HTTPException(400, "bad review")
    db.decide_change(change_id, body.review == "approved")
    return db.get_change(change_id)


class ItemCreate(EventFields):
    kind: str = "task"
    title: str
    owner: str | None = None
    due: str | None = None
    unit: str | None = None


@app.post("/api/chats/{chat_id}/items")
def create_item(chat_id: int, body: ItemCreate):
    _chat_or_404(chat_id)
    if body.kind not in ("task", "question", "decision", "event"):
        raise HTTPException(400, "bad kind")
    extra = _clean_event_fields(chat_id, body.model_dump(
        exclude_unset=True, exclude={"kind", "title", "owner", "due", "unit"}))
    if body.kind != "event" and any(k in extra for k in EVENT_ONLY):
        raise HTTPException(400, "event fields only apply to events")
    if body.kind == "event" and not extra.get("phase"):
        extra["phase"] = "idea"
    item_id = db.add_item(chat_id, body.kind, title=body.title.strip() or "?", owner=body.owner or None,
                          due=body.due or None, unit=body.unit or None, **extra)
    db.update_item(item_id, user=True)
    return db.get_item(item_id)


@app.delete("/api/items/{item_id}")
def delete_item(item_id: int):
    db.delete_item(item_id)
    return {"ok": True}


def _event_or_404(event_id: int) -> dict:
    ev = db.get_item(event_id)
    if not ev or ev["kind"] != "event":
        raise HTTPException(404, "event not found")
    return ev


def _report_view(ev: dict, row: dict | None) -> dict:
    if not row:
        return {"report": None}
    fresh = report.fingerprint(report.facts_text(ev, row["lang"])) == row["fingerprint"]
    return {"report": row["body"], "stale": not fresh, "source": row["source"], "model": row["model"],
            "created_at": row["created_at"]}


@app.get("/api/events/{event_id}/report")
def get_event_report(event_id: int):
    """The saved report, if any. `stale` = the event or its tasks/decisions changed since it was written."""
    ev = _event_or_404(event_id)
    return _report_view(ev, db.get_report(event_id))


@app.post("/api/events/{event_id}/report")
async def make_event_report(event_id: int):
    """Slow (local model): the UI shows elapsed time while this runs."""
    ev = _event_or_404(event_id)
    lang = report.language_of(ev["chat_id"])
    try:
        r = await report.generate(ev, lang)
    except llm.LLMError as e:
        raise HTTPException(503, str(e))
    except report.ReportRejected as e:
        raise HTTPException(422, {"message": "Rapor, kayıtlı veride olmayan sayı veya alıntı içerdiği için reddedildi / "
                                             "report rejected: it contained figures or quotations that are not in the recorded data",
                                  "unsupported": e.unsupported})
    db.save_report(event_id, r["report"], r["fingerprint"], lang, r["model"])
    return _report_view(ev, db.get_report(event_id))


@app.get("/api/events/{event_id}/page")
def event_page(event_id: int):
    """Everything recorded about one event, in one response. Linked = items whose event_id points here."""
    ev = _event_or_404(event_id)
    items = db.get_items(ev["chat_id"])
    today_s = today().isoformat()
    mine = [i for i in items if i["event_id"] == event_id]
    tasks = [{**i, "late": i["status"] == "open" and bool(i["due"]) and i["due"] < today_s}
             for i in mine if i["kind"] == "task"]
    meeting_ids = {i["meeting_id"] for i in mine if i["meeting_id"]}
    cards = [_meeting_card(m, items) for m in db.get_meetings(ev["chat_id"]) if m["id"] in meeting_ids]
    return {"event": ev, "today": today_s, "tasks": tasks,
            "decisions": [i for i in mine if i["kind"] == "decision"],
            "questions": [i for i in mine if i["kind"] == "question"],
            "meetings": cards, "attendance": analysis.event_row(ev),
            **_report_view(ev, db.get_report(event_id))}


@app.get("/api/chats/{chat_id}/people")
def people_list(chat_id: int):
    """People = owners of approved tasks. Counts only; no ranking."""
    chat = _chat_or_404(chat_id)
    return {"people": people.summary(db.get_items(chat_id), chat, today().isoformat())}


@app.get("/api/chats/{chat_id}/person")
def person(chat_id: int, name: str):
    chat = _chat_or_404(chat_id)
    items = db.get_items(chat_id)
    known = {people.key(n): n for n in people.names(items)}
    if people.key(name) not in known:
        raise HTTPException(404, "person not found")
    return people.detail(items, chat, db.get_meetings(chat_id), known[people.key(name)], today().isoformat())


@app.get("/api/chats/{chat_id}/event-analysis")
def event_analysis(chat_id: int):
    """Figures computed by code from approved events (no model). `insight` = the saved model comment, if any."""
    _chat_or_404(chat_id)
    stats = analysis.compute(db.get_items(chat_id))
    return {**stats, **analysis.insight_view(stats, db.get_insight(chat_id))}


@app.post("/api/chats/{chat_id}/event-analysis/insight")
async def event_insight(chat_id: int):
    """Slow (local model): the UI shows elapsed time. The text may only contain the computed figures."""
    _chat_or_404(chat_id)
    stats = analysis.compute(db.get_items(chat_id))
    if not stats["total"]:
        raise HTTPException(400, "Henüz etkinlik yok / no events yet")
    lang = report.language_of(chat_id)
    try:
        r = await analysis.generate(stats, lang)
    except llm.LLMError as e:
        raise HTTPException(503, str(e))
    except report.ReportRejected as e:
        raise HTTPException(422, {"message": "İçgörü, hesaplanan sayılarda olmayan rakamlar içerdiği için reddedildi / "
                                             "insight rejected: it contained figures that are not in the computed data",
                                  "unsupported": e.unsupported})
    db.save_insight(chat_id, r["insight"], r["fingerprint"], lang, r["model"])
    return {**stats, **analysis.insight_view(stats, db.get_insight(chat_id))}


@app.get("/api/chats/{chat_id}/unit")
def unit_page(chat_id: int, name: str):
    chat = _chat_or_404(chat_id)
    if name not in chat["units"]:
        raise HTTPException(404, "Komite bulunamadı / committee not found")
    return {**unitmod.page(chat_id, name, today().isoformat()), "report": unitmod.view(chat_id, name, today().isoformat())}


@app.post("/api/chats/{chat_id}/unit/report")
async def unit_report(chat_id: int, name: str):
    """Slow (local model). Saved in the database; goes stale when the committee's records change."""
    chat = _chat_or_404(chat_id)
    if name not in chat["units"]:
        raise HTTPException(404, "Komite bulunamadı / committee not found")
    try:
        r = await unitmod.generate(chat_id, name, today().isoformat(), report.language_of(chat_id) if db.get_messages(chat_id) else "tr")
    except llm.LLMError as e:
        raise HTTPException(503, str(e))
    except report.ReportRejected as e:
        raise HTTPException(422, {"message": "Rapor, veride olmayan rakamlar içerdiği için reddedildi / report rejected: figures not in the data",
                                  "unsupported": e.unsupported})
    db.save_unit_report(chat_id, name, r["report"], r["fingerprint"], "tr", r["model"])
    return unitmod.view(chat_id, name, today().isoformat())


# ---- meetings --------------------------------------------------------------------

LIMITS = {"title": 200, "attendees": 2000, "agenda": 5000, "notes": meetings.MAX_NOTES_BYTES}


class MeetingFields(BaseModel):
    title: str | None = None
    date: str | None = None       # "" = unknown
    time: str | None = None
    units: list[str] | None = None
    attendees: str | None = None
    agenda: str | None = None
    notes: str | None = None
    notes_source: str | None = None
    status: str | None = None


def _clean_meeting(chat_id: int, fields: dict) -> dict:
    """Blank text clears a field; date/time/status/committees are validated; no date is invented."""
    out = {}
    for k, v in fields.items():
        if isinstance(v, str):
            v = v.strip() or None
        out[k] = v
    for k, limit in LIMITS.items():
        if out.get(k) and len(out[k]) > limit:
            raise HTTPException(413 if k == "notes" else 400, f"{k}: en fazla {limit} karakter / at most {limit} characters")
    try:
        if "date" in out:
            out["date"] = meetings.valid_date(out["date"])
        if "time" in out:
            out["time"] = meetings.valid_time(out["time"])
    except ValueError as e:
        raise HTTPException(400, f"Geçersiz {e} / invalid {e}")
    if out.get("status") not in (None, *meetings.STATUSES):
        raise HTTPException(400, "bad status")
    if out.get("notes"):
        try:
            out["notes"] = meetings.clean_notes(out["notes"])
        except meetings.NotesError as e:
            raise HTTPException(400, str(e))
    if "units" in out:
        known = db.get_chat(chat_id)["units"]
        out["units"] = [u for u in dict.fromkeys(x.strip() for x in (out["units"] or [])) if u]
        if any(u not in known for u in out["units"]):
            raise HTTPException(400, "Komite bulunamadı / unknown committee")
    return out


def _meeting_or_404(meeting_id: int) -> dict:
    m = db.get_meeting(meeting_id)
    if not m:
        raise HTTPException(404, "meeting not found")
    return m


def _meeting_card(m: dict, items: list[dict]) -> dict:
    mine = [i for i in items if i["meeting_id"] == m["id"]]
    tasks = [i for i in mine if i["kind"] == "task"]
    return {**{k: v for k, v in m.items() if k != "notes"}, "has_notes": bool(m["notes"]),
            "tasks": len(tasks), "orphan_tasks": sum(1 for t in tasks if not t["owner"] and t["status"] == "open"),
            "decisions": sum(1 for i in mine if i["kind"] == "decision" and i["validity"] == "valid"),
            "questions": sum(1 for i in mine if i["kind"] == "question")}


@app.get("/api/chats/{chat_id}/meetings")
def list_meetings(chat_id: int):
    _chat_or_404(chat_id)
    items = db.get_items(chat_id)
    return [_meeting_card(m, items) for m in db.get_meetings(chat_id)]


@app.post("/api/chats/{chat_id}/meetings")
def create_meeting(chat_id: int, body: MeetingFields):
    _chat_or_404(chat_id)
    fields = _clean_meeting(chat_id, body.model_dump(exclude_unset=True))
    if not fields.get("title"):
        raise HTTPException(400, "Başlık gerekli / title is required")
    return db.get_meeting(db.add_meeting(chat_id, **fields))


@app.post("/api/chats/{chat_id}/meetings/notes-file")
async def meeting_notes_file(chat_id: int, request: Request, filename: str = ""):
    """Validate an uploaded .txt/.md and return its text; nothing is saved until the user saves the meeting."""
    _chat_or_404(chat_id)
    try:
        return {"text": meetings.decode_notes(await request.body(), filename), "filename": filename or None}
    except meetings.NotesError as e:
        raise HTTPException(400, str(e))


@app.get("/api/meetings/{meeting_id}")
def get_meeting(meeting_id: int):
    m = _meeting_or_404(meeting_id)
    mine = [i for i in db.get_items(m["chat_id"], review=None) if i["meeting_id"] == meeting_id]
    approved = [i for i in mine if i["review"] == "approved"]
    return {"meeting": m, "tasks": [i for i in approved if i["kind"] == "task"],
            "decisions": [i for i in approved if i["kind"] == "decision"],
            "questions": [i for i in approved if i["kind"] == "question"],
            "proposed": sum(1 for i in mine if i["review"] == "proposed"),
            "lines": len(meetings.note_lines(m["notes"])),
            "orphan_tasks": sum(1 for t in approved if t["kind"] == "task" and meetings.is_orphan(t)),
            "warnings": meetings.owner_warnings(m, db.get_chat(m["chat_id"]), [i for i in approved if i["kind"] == "task"]),
            "analyzed": m["analyzed_fp"] is not None,
            "notes_changed": m["analyzed_fp"] is not None and m["analyzed_fp"] != meetings.fingerprint(m["notes"])}


@app.post("/api/meetings/{meeting_id}/analyze")
async def analyze_meeting(meeting_id: int):
    """Slow (local model): the UI shows elapsed time. Results land in the AI review queue as suggestions."""
    _meeting_or_404(meeting_id)
    try:
        return await meetings.analyze(meeting_id)
    except meetings.NotesError as e:
        raise HTTPException(400, str(e))
    except llm.LLMError as e:
        raise HTTPException(503, str(e))


@app.get("/api/meetings/{meeting_id}/summary")
def get_meeting_summary(meeting_id: int):
    m = _meeting_or_404(meeting_id)
    return meetings.summary_view(m, db.get_meeting_summary(meeting_id))


@app.post("/api/meetings/{meeting_id}/summary")
async def make_meeting_summary(meeting_id: int):
    """Slow (local model): the UI shows elapsed time. Rejected when it contains figures or names not in the data."""
    m = _meeting_or_404(meeting_id)
    try:
        r = await meetings.summarize(m)
    except meetings.NotesError as e:
        raise HTTPException(400, str(e))
    except llm.LLMError as e:
        raise HTTPException(503, str(e))
    except report.ReportRejected as e:
        raise HTTPException(422, {"message": "Özet, kayıtlı veride olmayan sayı veya isimler içerdiği için reddedildi / "
                                             "summary rejected: it contained figures or names that are not in the recorded data",
                                  "unsupported": e.unsupported})
    db.save_meeting_summary(meeting_id, r["body"], r["fingerprint"], r["lang"], r["model"])
    return {**meetings.summary_view(m, db.get_meeting_summary(meeting_id)), "notes_cut": r["notes_cut"]}


@app.patch("/api/meetings/{meeting_id}")
def patch_meeting(meeting_id: int, body: MeetingFields):
    m = _meeting_or_404(meeting_id)
    fields = _clean_meeting(m["chat_id"], body.model_dump(exclude_unset=True))
    if "title" in fields and not fields["title"]:
        raise HTTPException(400, "Başlık boş olamaz / title cannot be empty")
    db.update_meeting(meeting_id, **fields)
    return db.get_meeting(meeting_id)


@app.delete("/api/meetings/{meeting_id}")
def delete_meeting(meeting_id: int):
    _meeting_or_404(meeting_id)
    db.delete_meeting(meeting_id)
    return {"ok": True}


SAMPLE_EVENT = ROOT / "demo" / "sample-event.json"


@app.post("/api/chats/{chat_id}/sample-event")
def sample_event(chat_id: int):
    """Add the shipped demo event (fake data) with its precomputed report: instant, no model needed."""
    _chat_or_404(chat_id)
    spec = json.loads(SAMPLE_EVENT.read_text(encoding="utf-8"))
    for e in db.get_items(chat_id, "event"):
        if e["title"] == spec["event"]["title"]:
            return {"event_id": e["id"], "created": False}
    ev = spec["event"]
    event_id = db.add_item(chat_id, "event", **ev)
    db.update_item(event_id, user=True)
    for t in spec["tasks"]:
        db.update_item(db.add_item(chat_id, "task", event_id=event_id, **t), user=True)
    for d in spec["decisions"]:
        db.update_item(db.add_item(chat_id, "decision", event_id=event_id, title=d), user=True)
    facts = report.facts_text(db.get_item(event_id), spec["lang"])
    db.save_report(event_id, spec["report"], report.fingerprint(facts), spec["lang"], spec.get("model"), "sample")
    return {"event_id": event_id, "created": True}


class SummaryReq(BaseModel):
    days: int = 7


@app.post("/api/chats/{chat_id}/summary")
async def summary(chat_id: int, body: SummaryReq):
    _chat_or_404(chat_id)
    try:
        r = await assistant.weekly_summary(chat_id, body.days)
        db.save_ai(chat_id, "recap", f"{today():%Y-%m-%d}", r, llm.MODEL)   # kept until deleted, shown on the next visit
        return r
    except llm.LLMError as e:
        raise HTTPException(503, str(e))


class AskReq(BaseModel):
    question: str


@app.post("/api/chats/{chat_id}/ask")
async def ask(chat_id: int, body: AskReq):
    _chat_or_404(chat_id)
    try:
        return await assistant.ask(chat_id, body.question)
    except llm.LLMError as e:
        raise HTTPException(503, str(e))


app.mount("/", StaticFiles(directory=ROOT / "static", html=True), name="static")
