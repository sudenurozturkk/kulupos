"""Pano HTTP API + static UI. Binds to localhost only."""
from __future__ import annotations

import asyncio
import contextlib
import hashlib
import os
import re
from datetime import date, timedelta
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import PlainTextResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from . import analyzer, assistant, db, insights, llm
from .parser import MAX_BYTES, parse_report, read_export

ROOT = Path(__file__).resolve().parent.parent
DEMOS = {
    "tr": ("KBK Yönetim 2026", ROOT / "demo" / "kbk-yonetim-tr.txt",
           ["Yönetim", "Etkinlik", "Sosyal Medya", "Sponsorluk", "Teknik"]),
    "en": ("Robotics Club Board", ROOT / "demo" / "robotics-club-en.txt",
           ["Board", "Events", "Social Media", "Sponsorship", "Tech"]),
}

@contextlib.asynccontextmanager
async def lifespan(_: FastAPI):
    db.recover_stale_analyses()
    yield


app = FastAPI(title="Pano", docs_url="/api/docs", lifespan=lifespan)
_tasks: set[asyncio.Task] = set()


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


def _import(data: bytes, name: str, units: list[str]) -> dict:
    messages, _ = _read(data)
    chat_id = db.create_chat(name, units, messages, hashlib.sha256(data).hexdigest())
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
def chats():
    return db.list_chats()


@app.post("/api/chats")
async def upload(request: Request, filename: str = "chat.txt", name: str = "", units: str = ""):
    data = await request.body()
    unit_list = [u.strip() for u in units.split(",") if u.strip()]
    return _import(data, name.strip() or _name_from_filename(filename), unit_list)


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


@app.post("/api/demo/{lang}")
def demo(lang: str):
    if lang not in DEMOS:
        raise HTTPException(404)
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
        "review": db.get_items(chat_id, review="proposed"),  # AI suggestions awaiting approval
        "changes": db.get_changes(chat_id),  # AI edits to approved items awaiting approval
        "overview": insights.overview(chat, items, db.senders(chat_id), t),
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


class PlanAccept(BaseModel):
    event_title: str | None = None
    event_date: str | None = None
    tasks: list[dict]


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
    return {"added": len(body.tasks)}


@app.get("/api/chats/{chat_id}/export.md", response_class=PlainTextResponse)
def export_md(chat_id: int):
    """The whole board as Markdown, with source references, for Notion/GitHub/Docs."""
    b = board(chat_id)
    out = [f"# {b['chat']['name']}", "", f"_Pano · {b['today']}_", "", "## Tasks", ""]
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


@app.get("/api/chats/{chat_id}/messages")
def messages(chat_id: int, around: int, radius: int = 4):
    _chat_or_404(chat_id)
    return db.get_messages(chat_id, max(0, around - radius), around + radius)


PHASES = ("idea", "planning", "confirmed", "held", "cancelled")
NUMERIC = ("attendees_expected", "attendees_actual", "budget_est", "budget_actual")
EVENT_ONLY = ("phase", "event_type", "event_units", *NUMERIC)


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


@app.patch("/api/items/{item_id}")
def patch_item(item_id: int, body: ItemPatch):
    if not db.get_item(item_id):
        raise HTTPException(404)
    # "" clears a field; omitted fields stay untouched.
    cur = db.get_item(item_id)
    fields = {k: (None if v == "" else v) for k, v in body.model_dump(exclude_unset=True).items()}
    fields = _clean_event_fields(cur["chat_id"], fields)
    if cur["kind"] != "event" and any(k in fields for k in EVENT_ONLY):
        raise HTTPException(400, "event fields only apply to events")
    if fields.get("event_id") == item_id:
        raise HTTPException(400, "an event cannot link to itself")
    for required in ("title", "status"):
        if fields.get(required, "") is None:
            del fields[required]
    if fields.get("status") not in (None, "open", "done", "answered"):
        raise HTTPException(400, "bad status")
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


class SummaryReq(BaseModel):
    days: int = 7


@app.post("/api/chats/{chat_id}/summary")
async def summary(chat_id: int, body: SummaryReq):
    _chat_or_404(chat_id)
    try:
        return await assistant.weekly_summary(chat_id, body.days)
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
