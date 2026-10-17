"""Turns a WhatsApp chat into a task board, one window of messages at a time.

Each window is sent to Gemma together with the *current* board state, so the
model can not only find new tasks but also close, reassign or reschedule old
ones ("afişi bitirdim", "söyleşi 31 Ekim'e kaydı"). That running state is what
keeps the board honest when plans change mid-chat.
"""
from __future__ import annotations

import asyncio
import os
import re
import time
from datetime import date, datetime, timedelta
from difflib import SequenceMatcher

from . import db, llm

CHUNK = int(os.environ.get("PANO_CHUNK", "30"))
CONTEXT = 4  # already-processed messages shown before each window
WEEKDAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

_s = {"type": "string"}
_i = {"type": "integer"}


def _obj(**props) -> dict:
    return {"type": "object", "properties": props, "required": list(props)}


SCHEMA = _obj(
    new_tasks={"type": "array", "items": _obj(source=_i, title=_s, owner=_s, due=_s, unit=_s)},
    task_updates={"type": "array", "items": _obj(
        source=_i, id=_i, status={"type": "string", "enum": ["open", "done"]}, owner=_s, due=_s)},
    new_questions={"type": "array", "items": _obj(source=_i, text=_s, asked_by=_s)},
    answered_questions={"type": "array", "items": _obj(source=_i, id=_i)},
    decisions={"type": "array", "items": _obj(source=_i, text=_s)},
    new_events={"type": "array", "items": _obj(source=_i, title=_s, date=_s, time=_s, place=_s)},
    event_updates={"type": "array", "items": _obj(source=_i, id=_i, date=_s, time=_s, place=_s)},
)

SYSTEM = """You are Pano, the organiser of a student club. You read the club's WhatsApp group \
chat in small batches and keep the club's board up to date. You get the club units, the members, \
the current board (open tasks T#, open questions Q#, events E#) and a batch of NEW MESSAGES, \
each with an id like [#12].

Extract ONLY what appears in the NEW MESSAGES:
- new_tasks: a concrete piece of work someone committed to ("ben hallederim", "I'll do it") \
or was asked to do. Not wishes, jokes, personal plans or chit-chat (films, matches, lessons, food). \
owner = the member's full name as listed in MEMBERS; if a person volunteers, the owner is the \
sender. If nobody took it, owner = "". due = YYYY-MM-DD resolved with the CALENDAR, or "". \
unit = one of UNITS that fits the work, or "". title = short, max 8 words.
- task_updates: a message finishes ("verdim ✅", "hazır", "done"), reassigns or reschedules an \
EXISTING open task -> use its T id. Do not repeat a task that already exists as a new task.
- new_questions: a question to the group about club work that needs an answer.
- answered_questions: a NEW message answers an existing open question -> its Q id.
- decisions: a final agreement of the group ("karar: ...", "tamam o zaman ... yapıyoruz").
- new_events: a scheduled club event or meeting with a date. event_updates: an existing E# \
event got a new date/time/place.
source = the id of the message the item comes from. Write every text in the language of the chat.
Empty lists are fine. Never invent people, dates or ids."""


# ---- helpers ---------------------------------------------------------------

_TR = str.maketrans("İIıŞşĞğÜüÖöÇç", "iiissgguuoocc")


def norm(s: str) -> str:
    return re.sub(r"[^\w\s]", " ", (s or "").translate(_TR).lower()).strip()


def similar(a: str, b: str) -> float:
    return SequenceMatcher(None, norm(a), norm(b)).ratio()


def detect_lang(messages: list[dict]) -> str:
    text = " ".join(m["text"] for m in messages[:200]).lower()
    tr_hits = sum(text.count(c) for c in "ışğçöü") + len(re.findall(r"\b(ve|bir|bu|ben|mi|da|de)\b", text))
    en_hits = len(re.findall(r"\b(the|and|is|you|to|we|i)\b", text))
    return "tr" if tr_hits >= en_hits else "en"


def fmt_ts(ts: str) -> str:
    d = datetime.fromisoformat(ts)
    return f"{WEEKDAYS[d.weekday()]} {d:%Y-%m-%d %H:%M}"


def render_messages(msgs: list[dict]) -> str:
    lines = []
    for m in msgs:
        if m["kind"] in ("system", "deleted"):
            continue
        text = "<media>" if m["kind"] == "media" else m["text"][:600].replace("\n", " / ")
        lines.append(f"[#{m['idx']}] {fmt_ts(m['ts'])} {m['sender']}: {text}")
    return "\n".join(lines)


def calendar(start: date, days: int = 21) -> str:
    return ", ".join(f"{WEEKDAYS[d.weekday()]} {d.isoformat()}"
                     for d in (start + timedelta(n) for n in range(days)))


def match_member(name: str, members: list[str]) -> str | None:
    if not name or not name.strip():
        return None
    n = norm(name)
    for m in members:
        if norm(m) == n:
            return m
    first = [m for m in members if norm(m).split()[0] == n.split()[0]] if n else []
    if len(first) == 1:
        return first[0]
    best = max(members, key=lambda m: similar(m, name), default=None)
    if best and similar(best, name) > 0.8:
        return best
    return name.strip()  # someone outside the member list (e.g. a speaker)


def match_unit(unit: str, units: list[str]) -> str | None:
    if not unit:
        return None
    for u in units:
        if norm(u) == norm(unit):
            return u
    partial = [u for u in units if norm(unit) in norm(u) or norm(u) in norm(unit)]
    if len(partial) == 1:
        return partial[0]  # "Sosyal" -> "Sosyal Medya"
    best = max(units, key=lambda u: similar(u, unit), default=None)
    return best if best and similar(best, unit) > 0.7 else None


def valid_date(s: str, around: date) -> str | None:
    s = (s or "").strip()
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", s):
        return None
    try:
        d = date.fromisoformat(s)
    except ValueError:
        return None
    return s if around - timedelta(60) <= d <= around + timedelta(365) else None


def board_state(chat_id: int) -> str:
    items = db.get_items(chat_id)
    tasks = [i for i in items if i["kind"] == "task" and i["status"] == "open"]
    questions = [i for i in items if i["kind"] == "question" and i["status"] == "open"]
    events = [i for i in items if i["kind"] == "event"]
    out = ["OPEN TASKS:"]
    out += [f"T{t['id']} | {t['title']} | owner: {t['owner'] or '-'} | due: {t['due'] or '-'} | "
            f"unit: {t['unit'] or '-'}" for t in tasks] or ["(none)"]
    out.append("OPEN QUESTIONS:")
    out += [f"Q{q['id']} | {q['title']} | asked by {q['owner'] or '-'}" for q in questions] or ["(none)"]
    out.append("EVENTS:")
    out += [f"E{e['id']} | {e['title']} | {e['due'] or '-'} {e['time'] or ''} | {e['place'] or '-'}"
            for e in events] or ["(none)"]
    return "\n".join(out)


# ---- progress (in memory, polled by the UI) ---------------------------------

PROGRESS: dict[int, dict] = {}
_run_lock = asyncio.Lock()  # one model, one analysis at a time


def progress(chat_id: int) -> dict:
    return PROGRESS.get(chat_id, {"state": "idle"})


# ---- the analysis loop -----------------------------------------------------

async def analyze(chat_id: int) -> None:
    chat = db.get_chat(chat_id)
    start = chat["analyzed_upto"] + 1
    msgs = db.get_messages(chat_id, start)
    windows = [msgs[i:i + CHUNK] for i in range(0, len(msgs), CHUNK)]
    PROGRESS[chat_id] = {"state": "queued", "done": 0, "total": len(windows), "found": [],
                         "started": time.time(), "error": None}
    async with _run_lock:
        PROGRESS[chat_id]["state"] = "running"
        db.update_chat(chat_id, status="analyzing", error=None)
        try:
            for n, window in enumerate(windows):
                await _process_window(chat_id, chat, window)
                db.update_chat(chat_id, analyzed_upto=window[-1]["idx"])
                PROGRESS[chat_id]["done"] = n + 1
            db.update_chat(chat_id, status="ready")
            PROGRESS[chat_id]["state"] = "done"
        except Exception as e:  # surface any failure to the UI instead of dying silently
            db.update_chat(chat_id, status="error", error=str(e))
            PROGRESS[chat_id].update(state="error", error=str(e))


async def _process_window(chat_id: int, chat: dict, window: list[dict]) -> None:
    if not any(m["kind"] in ("text", "media") for m in window):
        return
    members = db.senders(chat_id)
    units = chat["units"]
    first = window[0]["idx"]
    context = db.get_messages(chat_id, max(0, first - CONTEXT), first - 1) if first else []
    day0 = datetime.fromisoformat(window[0]["ts"]).date()
    last_day = datetime.fromisoformat(window[-1]["ts"]).date()

    prompt = "\n".join([
        f"UNITS: {', '.join(units) or '(none)'}",
        f"MEMBERS: {', '.join(members)}",
        f"CALENDAR: {calendar(day0 - timedelta(day0.weekday()), (last_day - day0).days + 28)}",
        "",
        board_state(chat_id),
        "",
        "EARLIER MESSAGES (context only, already processed):",
        render_messages(context) or "(none)",
        "",
        "NEW MESSAGES:",
        render_messages(window),
    ])
    msgs = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": prompt}]
    try:
        result = await llm.chat_json(msgs, SCHEMA)
    except (llm.LLMError, ValueError):
        result = await llm.chat_json(msgs, SCHEMA, temperature=0.3)  # one retry, slightly varied
    _apply(chat_id, result, window, members, units, last_day)


def _apply(chat_id: int, r: dict, window: list[dict], members: list[str], units: list[str],
           around: date) -> None:
    valid_src = {m["idx"] for m in window}
    found = PROGRESS.setdefault(chat_id, {}).setdefault("found", [])
    items = db.get_items(chat_id)
    by_id = {i["id"]: i for i in items}

    def src(x):
        return x.get("source") if x.get("source") in valid_src else None

    def note(kind, text):
        found.append({"kind": kind, "text": text})
        del found[:-12]

    # Updates first, so a task finished in this window is not re-added as new.
    for u in r.get("task_updates", []):
        t = by_id.get(u.get("id"))
        if not t or t["kind"] != "task" or t["user_edited"]:
            continue
        changes = {}
        if u.get("status") == "done" and t["status"] != "done":
            changes.update(status="done", resolved_idx=src(u))
        owner = match_member(u.get("owner", ""), members)
        if owner and owner != t["owner"]:
            changes["owner"] = owner
        due = valid_date(u.get("due", ""), around)
        if due and due != t["due"]:
            changes["due"] = due
        if changes:
            db.update_item(t["id"], **changes)
            note("update", t["title"])

    tasks = db.get_items(chat_id, "task")  # done ones too: a finished task must not come back
    for t in r.get("new_tasks", []):
        title = (t.get("title") or "").strip()
        if not title:
            continue
        dup = next((o for o in tasks if similar(o["title"], title) > 0.75), None)
        owner = match_member(t.get("owner", ""), members)
        due = valid_date(t.get("due", ""), around)
        if dup:
            if not dup["user_edited"]:
                fill = {k: v for k, v in (("owner", owner), ("due", due)) if v and not dup[k]}
                if fill:
                    db.update_item(dup["id"], **fill)
            continue
        new_id = db.add_item(chat_id, "task", title=title, owner=owner, due=due,
                             unit=match_unit(t.get("unit", ""), units), source_idx=src(t))
        tasks.append(db.get_item(new_id))
        note("task", title)

    for a in r.get("answered_questions", []):
        q = by_id.get(a.get("id"))
        if q and q["kind"] == "question" and q["status"] == "open":
            db.update_item(q["id"], status="answered", resolved_idx=src(a))

    questions = db.get_items(chat_id, "question")
    for q in r.get("new_questions", []):
        text = (q.get("text") or "").strip()
        if not text or any(similar(o["title"], text) > 0.7 for o in questions):
            continue
        new_id = db.add_item(chat_id, "question", title=text,
                             owner=match_member(q.get("asked_by", ""), members), source_idx=src(q))
        questions.append(db.get_item(new_id))
        note("question", text)

    decisions = db.get_items(chat_id, "decision")
    for d in r.get("decisions", []):
        text = (d.get("text") or "").strip()
        if not text or any(similar(o["title"], text) > 0.7 for o in decisions):
            continue
        new_id = db.add_item(chat_id, "decision", title=text, source_idx=src(d))
        decisions.append(db.get_item(new_id))
        note("decision", text)

    for u in r.get("event_updates", []):
        e = by_id.get(u.get("id"))
        if not e or e["kind"] != "event" or e["user_edited"]:
            continue
        changes = {k: v for k, v in (
            ("due", valid_date(u.get("date", ""), around)),
            ("time", (u.get("time") or "").strip() or None),
            ("place", (u.get("place") or "").strip() or None)) if v and v != e[k]}
        if changes:
            db.update_item(e["id"], **changes)
            note("update", e["title"])

    events = db.get_items(chat_id, "event")
    for ev in r.get("new_events", []):
        title = (ev.get("title") or "").strip()
        when = valid_date(ev.get("date", ""), around)
        if not title or not when:
            continue
        dup = next((o for o in events if similar(o["title"], title) > 0.6), None)
        if dup:
            if not dup["user_edited"] and dup["due"] != when:
                db.update_item(dup["id"], due=when, time=(ev.get("time") or "").strip() or dup["time"])
            continue
        new_id = db.add_item(chat_id, "event", title=title, due=when,
                             time=(ev.get("time") or "").strip() or None,
                             place=(ev.get("place") or "").strip() or None, source_idx=src(ev))
        events.append(db.get_item(new_id))
        note("event", title)
