"""First-run sample club: fake data only, flagged as sample, removable in one call."""
from __future__ import annotations

import json
from datetime import timedelta
from pathlib import Path

from . import db
from .analyzer import norm
from .parser import parse_chat, read_export

DEMO = Path(__file__).resolve().parent.parent / "demo"
SPEC = DEMO / "seed-panel-tr.json"


def _squash(s: str) -> str:
    return " ".join(norm(s).split())


def seed_sample(today) -> int | None:
    """Create the sample club unless the database already has chats or the user cleared it before."""
    if db.list_chats() or db.get_meta("sample_dismissed"):
        return None
    spec = json.loads(SPEC.read_text(encoding="utf-8"))
    c = spec["chat"]
    messages = parse_chat(read_export((DEMO / c["messages_file"]).read_bytes()))
    chat_id = db.create_chat(c["name"], c["units"], messages, source_name=c["source_name"], is_sample=True)
    texts = [(i, _squash(m.text)) for i, m in enumerate(messages) if m.sender]

    def find(phrase):
        key = _squash(phrase) if phrase else ""
        return next((i for i, t in texts if key and key in t), None)

    def due(offset):
        return None if offset is None else (today + timedelta(days=offset)).isoformat()

    events = {}
    for e in spec["events"]:
        events[e["key"]] = db.add_item(
            chat_id, "event", title=e["title"], due=due(e["due"]), time=e["time"], place=e["place"],
            owner=e["owner"], event_type=e["event_type"], phase=e["phase"], event_units=e["event_units"],
            source_idx=find(e["src"]))
    for t in spec["tasks"]:
        db.add_item(chat_id, "task", title=t["title"], owner=t.get("owner"), unit=t.get("unit"),
                    due=due(t.get("due")), status=t.get("status", "open"), source_idx=find(t["src"]),
                    event_id=events.get(t.get("event")))
    for q in spec["questions"]:
        db.add_item(chat_id, "question", title=q["title"], owner=q.get("owner"), status=q.get("status", "open"),
                    source_idx=find(q["src"]), resolved_idx=find(q.get("resolved")))
    for d in spec["decisions"]:
        db.add_item(chat_id, "decision", title=d["title"], status=d.get("status", "open"),
                    source_idx=find(d["src"]), event_id=events.get(d.get("event")))
    for p in spec["proposed"]:
        db.add_item(chat_id, p["kind"], review="proposed", title=p["title"], owner=p.get("owner"),
                    unit=p.get("unit"), source_idx=find(p.get("src")), needs_review=p.get("needs_review", 0))
    db.update_chat(chat_id, status="ready", analyzed_upto=len(messages) - 1)
    return chat_id


def clear_sample() -> int:
    """Delete every sample club and remember not to bring it back."""
    removed = db.delete_samples()
    db.set_meta("sample_dismissed", "1")
    return removed
