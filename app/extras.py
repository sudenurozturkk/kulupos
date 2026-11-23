"""Extra endpoints: universal search, iCalendar (.ics) export and task comments.

Everything here reads approved records only (AI proposals are not real records yet)."""
from __future__ import annotations

import hashlib
import re
from datetime import date, datetime, timedelta, timezone

from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel

from . import db

router = APIRouter()

MAX_Q = 100
PER_GROUP = 15
KIND_LABEL = {"task": "Görev", "decision": "Karar", "question": "Soru", "event": "Etkinlik"}


# ---- search ----------------------------------------------------------------

def fold(s: str | None) -> str:
    """Case/accents-insensitive form for Turkish and English text (İ/I/ı all match i)."""
    s = (s or "").replace("İ", "i").replace("I", "i").replace("ı", "i").lower()
    for a, b in (("ç", "c"), ("ğ", "g"), ("ö", "o"), ("ş", "s"), ("ü", "u")):
        s = s.replace(a, b)
    return s


def snippet(text: str, needle: str, width: int = 60) -> str:
    text = re.sub(r"\s+", " ", text or "").strip()
    pos = fold(text).find(needle)
    if pos < 0 or len(text) <= 2 * width:
        return text[: 2 * width] + ("…" if len(text) > 2 * width else "")
    a, b = max(0, pos - width), min(len(text), pos + len(needle) + width)
    return ("…" if a else "") + text[a:b] + ("…" if b < len(text) else "")


def search(chat_id: int, q: str) -> dict:
    needle = fold(q.strip())
    out: dict[str, list] = {"items": [], "meetings": [], "messages": []}
    if len(needle) < 2:
        return out
    for it in db.get_items(chat_id):
        hay = " ".join(str(it.get(k) or "") for k in ("title", "owner", "unit", "place", "notes"))
        if needle in fold(hay) and len(out["items"]) < PER_GROUP:
            out["items"].append({"id": it["id"], "kind": it["kind"], "title": it["title"], "owner": it.get("owner"),
                                 "due": it.get("due"), "status": it.get("status"), "event_id": it.get("event_id"),
                                 "snippet": snippet(it.get("notes") or it["title"], needle)})
    for m in db.get_meetings(chat_id):
        hay = " ".join(str(m.get(k) or "") for k in ("title", "agenda", "notes", "attendees"))
        if needle in fold(hay) and len(out["meetings"]) < PER_GROUP:
            out["meetings"].append({"id": m["id"], "title": m["title"], "date": m.get("date"), "status": m.get("status"),
                                    "snippet": snippet(m.get("notes") or m.get("agenda") or m["title"], needle)})
    for msg in db.get_messages(chat_id):
        if msg["kind"] == "text" and needle in fold(msg["text"] + " " + (msg["sender"] or "")):
            out["messages"].append({"idx": msg["idx"], "ts": msg["ts"], "sender": msg["sender"],
                                    "snippet": snippet(msg["text"], needle)})
            if len(out["messages"]) >= PER_GROUP:
                break
    return out


@router.get("/api/chats/{chat_id}/search")
def search_chat(chat_id: int, q: str = ""):
    if not db.get_chat(chat_id):
        raise HTTPException(404, "chat not found")
    q = q.strip()
    if len(q) > MAX_Q:
        raise HTTPException(400, f"Arama en çok {MAX_Q} karakter / search is limited to {MAX_Q} characters")
    res = search(chat_id, q)
    res["query"] = q
    res["total"] = sum(len(v) for k, v in res.items() if isinstance(v, list))
    return res


# ---- iCalendar -------------------------------------------------------------

def _esc(s: str) -> str:
    return (s or "").replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\r", "").replace("\n", "\\n")


def _fold_line(line: str) -> str:
    raw, out = line.encode("utf-8"), []
    while len(raw) > 74:
        cut = 74
        while cut > 0 and (raw[cut] & 0xC0) == 0x80:   # never split a multi-byte character
            cut -= 1
        out.append(raw[:cut].decode("utf-8"))
        raw = b" " + raw[cut:]
    out.append(raw.decode("utf-8"))
    return "\r\n".join(out)


def _day(v: str | None) -> date | None:
    try:
        return date.fromisoformat((v or "")[:10])
    except ValueError:
        return None


def _clock(v: str | None) -> tuple[int, int] | None:
    m = re.fullmatch(r"\s*(\d{1,2})[:.](\d{2})\s*", v or "")
    if m and int(m.group(1)) < 24 and int(m.group(2)) < 60:
        return int(m.group(1)), int(m.group(2))
    return None


def _vevent(uid: str, summary: str, day: date, time: str | None, place: str | None = None, desc: str | None = None,
            stamp: str = "") -> list[str]:
    lines = ["BEGIN:VEVENT", f"UID:{uid}@kulupos", f"DTSTAMP:{stamp}"]
    clock = _clock(time)
    if clock:
        start = datetime(day.year, day.month, day.day, *clock)
        end = start + timedelta(hours=1)
        lines += [f"DTSTART:{start:%Y%m%dT%H%M%S}", f"DTEND:{end:%Y%m%dT%H%M%S}"]   # floating local time
    else:
        lines += [f"DTSTART;VALUE=DATE:{day:%Y%m%d}", f"DTEND;VALUE=DATE:{day + timedelta(days=1):%Y%m%d}"]
    lines.append(f"SUMMARY:{_esc(summary)}")
    if place:
        lines.append(f"LOCATION:{_esc(place)}")
    if desc:
        lines.append(f"DESCRIPTION:{_esc(desc)}")
    lines.append("END:VEVENT")
    return lines


def build_ics(chat_id: int, include_tasks: bool = True, now: datetime | None = None) -> str:
    chat = db.get_chat(chat_id)
    stamp = (now or datetime.now(timezone.utc)).strftime("%Y%m%dT%H%M%SZ")
    lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//KulupOS//TR", "CALSCALE:GREGORIAN",
             f"X-WR-CALNAME:{_esc(chat['name'])}"]
    for it in db.get_items(chat_id):
        day = _day(it.get("due"))
        if not day:
            continue
        if it["kind"] == "event" and it.get("phase") != "cancelled":
            lines += _vevent(f"event-{it['id']}", it["title"], day, it.get("time"), it.get("place"), it.get("notes"), stamp)
        elif it["kind"] == "task" and include_tasks and it.get("status") != "done":
            who = f"Sorumlu: {it['owner']}" if it.get("owner") else None
            lines += _vevent(f"task-{it['id']}", "Görev: " + it["title"], day, None, None, who, stamp)
    for m in db.get_meetings(chat_id):
        day = _day(m.get("date"))
        if day and m.get("status") != "cancelled":
            lines += _vevent(f"meeting-{m['id']}", "Toplantı: " + m["title"], day, m.get("time"), None, m.get("agenda"), stamp)
    lines.append("END:VCALENDAR")
    return "\r\n".join(_fold_line(x) for x in lines) + "\r\n"


@router.get("/api/chats/{chat_id}/calendar.ics")
def calendar_ics(chat_id: int, tasks: bool = True):
    if not db.get_chat(chat_id):
        raise HTTPException(404, "chat not found")
    return Response(build_ics(chat_id, tasks), media_type="text/calendar; charset=utf-8",
                    headers={"Content-Disposition": 'attachment; filename="kulupos.ics"'})


# ---- task comments ---------------------------------------------------------

class Comment(BaseModel):
    text: str


@router.post("/api/items/{item_id}/comments")
def add_comment(item_id: int, body: Comment):
    if not db.get_item(item_id):
        raise HTTPException(404)
    text = body.text.strip()
    if not text:
        raise HTTPException(400, "Yorum boş olamaz / the comment is empty")
    if len(text) > 500:
        raise HTTPException(400, "Yorum en çok 500 karakter / comments are limited to 500 characters")
    db.add_history(item_id, "comment", None, None, text)
    return db.get_history(item_id)
