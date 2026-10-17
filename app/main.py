"""Pano HTTP API + static UI. Binds to localhost only."""
from __future__ import annotations

import asyncio
import os
import re
from datetime import date, timedelta
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from . import analyzer, assistant, db, llm
from .parser import parse_chat, read_export

ROOT = Path(__file__).resolve().parent.parent
DEMOS = {
    "tr": ("KBK Yönetim 2026", ROOT / "demo" / "kbk-yonetim-tr.txt",
           ["Yönetim", "Etkinlik", "Sosyal Medya", "Sponsorluk", "Teknik"]),
    "en": ("Robotics Club Board", ROOT / "demo" / "robotics-club-en.txt",
           ["Board", "Events", "Social Media", "Sponsorship", "Tech"]),
}

app = FastAPI(title="Pano", docs_url="/api/docs")
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


def _import(data: bytes, name: str, units: list[str]) -> dict:
    try:
        messages = parse_chat(read_export(data))
    except Exception as e:
        raise HTTPException(400, f"Dosya okunamadı / could not read file: {e}")
    if not any(m.sender for m in messages):
        raise HTTPException(400, "Bu bir WhatsApp sohbet dışa aktarımı gibi görünmüyor / "
                                 "this does not look like a WhatsApp export")
    chat_id = db.create_chat(name, units, messages)
    return db.get_chat(chat_id)


def _start_analysis(chat_id: int) -> None:
    if analyzer.progress(chat_id).get("state") in ("queued", "running"):
        return
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
    if not data:
        raise HTTPException(400, "empty upload")
    unit_list = [u.strip() for u in units.split(",") if u.strip()]
    return _import(data, name.strip() or _name_from_filename(filename), unit_list)


@app.post("/api/demo/{lang}")
def demo(lang: str):
    if lang not in DEMOS:
        raise HTTPException(404)
    name, path, units = DEMOS[lang]
    return _import(path.read_bytes(), name, units)


@app.post("/api/chats/{chat_id}/import")
async def reimport(chat_id: int, request: Request):
    """Upload a newer export of the same group: only new messages are added and analysed."""
    _chat_or_404(chat_id)
    added = db.append_messages(chat_id, parse_chat(read_export(await request.body())))
    if added:
        _start_analysis(chat_id)
    return {"added": added}


class ChatPatch(BaseModel):
    name: str | None = None
    units: list[str] | None = None


@app.patch("/api/chats/{chat_id}")
def patch_chat(chat_id: int, body: ChatPatch):
    _chat_or_404(chat_id)
    fields = body.model_dump(exclude_none=True)
    if fields:
        db.update_chat(chat_id, **fields)
    return db.get_chat(chat_id)


@app.delete("/api/chats/{chat_id}")
def delete_chat(chat_id: int):
    db.delete_chat(chat_id)
    return {"ok": True}


@app.post("/api/chats/{chat_id}/analyze")
def analyze(chat_id: int, reset: bool = False):
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
        "progress": analyzer.progress(chat_id),
    }


@app.get("/api/chats/{chat_id}/messages")
def messages(chat_id: int, around: int, radius: int = 4):
    _chat_or_404(chat_id)
    return db.get_messages(chat_id, max(0, around - radius), around + radius)


class ItemPatch(BaseModel):
    title: str | None = None
    owner: str | None = None
    due: str | None = None
    unit: str | None = None
    status: str | None = None


@app.patch("/api/items/{item_id}")
def patch_item(item_id: int, body: ItemPatch):
    if not db.get_item(item_id):
        raise HTTPException(404)
    # "" clears a field; omitted fields stay untouched.
    fields = {k: (v or None) for k, v in body.model_dump(exclude_unset=True).items()}
    for required in ("title", "status"):
        if fields.get(required, "") is None:
            del fields[required]
    if fields.get("status") not in (None, "open", "done", "answered"):
        raise HTTPException(400, "bad status")
    db.update_item(item_id, user=True, **fields)
    return db.get_item(item_id)


class ItemCreate(BaseModel):
    kind: str = "task"
    title: str
    owner: str | None = None
    due: str | None = None
    unit: str | None = None


@app.post("/api/chats/{chat_id}/items")
def create_item(chat_id: int, body: ItemCreate):
    _chat_or_404(chat_id)
    item_id = db.add_item(chat_id, body.kind, title=body.title, owner=body.owner or None,
                          due=body.due or None, unit=body.unit or None)
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
