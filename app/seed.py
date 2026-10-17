"""First-run sample club: fake data only, flagged as sample, removable in one call."""
from __future__ import annotations

import json
from datetime import timedelta
from pathlib import Path

from . import analysis, db, meetings, report
from .analyzer import norm
from .parser import parse_chat, read_export

DEMO = Path(__file__).resolve().parent.parent / "demo"
SPEC = DEMO / "seed-panel-tr.json"
INSIGHT = DEMO / "seed-insight-tr.json"
MEETINGS = DEMO / "seed-meetings-tr.json"
MEETING_SUMMARY = DEMO / "seed-meeting-summary-tr.json"


def _squash(s: str) -> str:
    return " ".join(norm(s).split())


def seed_sample(today, force: bool = False) -> int | None:
    """Create the sample club unless the database already has chats or the user cleared it before.
    force=True (the user clicked "demo") skips both checks."""
    if not force and (db.list_chats() or db.get_meta("sample_dismissed")):
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
            source_idx=find(e["src"]),
            **{k: e[k] for k in ("attendees_expected", "attendees_actual", "applications", "budget_est",
                                 "budget_actual", "feedback_score", "feedback_note") if k in e})
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
    _seed_insight(chat_id)
    _seed_meetings(chat_id, today)
    db.update_chat(chat_id, status="ready", analyzed_upto=len(messages) - 1)
    return chat_id


def ensure_sample(today) -> int:
    """The sample club for an explicit "open the demo" click: reuse the existing one, else create it. No model."""
    rows = db._rows("SELECT id FROM chats WHERE is_sample = 1 ORDER BY id LIMIT 1")
    if not rows:
        return seed_sample(today, force=True)
    if not db.get_meetings(rows[0]["id"]):  # a sample made before meetings existed gets the two sample meetings
        _seed_meetings(rows[0]["id"], today)
    return rows[0]["id"]


def _seed_insight(chat_id: int) -> None:
    """Precomputed period comment (written once by scripts/make_sample_insight.py with the local model)."""
    if not INSIGHT.exists():
        return
    spec = json.loads(INSIGHT.read_text(encoding="utf-8"))
    facts = analysis.facts_text(analysis.compute(db.get_items(chat_id)), spec["lang"])
    db.save_insight(chat_id, spec["insight"], report.fingerprint(facts), spec["lang"], spec.get("model"), "sample")


def _seed_meetings(chat_id: int, today) -> None:
    """Two fake meetings: one held (notes, linked records, precomputed summary), one planned. The held one has a fixed
    past date so the summary stays true; the planned one is always a few days ahead."""
    if not MEETINGS.exists():
        return
    spec = json.loads(MEETINGS.read_text(encoding="utf-8"))
    db.update_chat(chat_id, unit_members=spec["unit_members"])
    made = {}
    for m in spec["meetings"]:
        when = m.get("date") or (today + timedelta(days=m["date_offset"])).isoformat()
        notes = m.get("notes")
        mid = made[m["key"]] = db.add_meeting(
            chat_id, title=m["title"], date=when, time=m["time"], status=m["status"], units=m["units"],
            attendees=m["attendees"], agenda=m.get("agenda"), notes=notes,
            analyzed_fp=meetings.fingerprint(notes) if m.get("proposed") else None)  # its suggestions are precomputed
        lines = meetings.note_lines(notes)

        def quote(phrase):
            key = _squash(phrase) if phrase else ""
            return next((ln[:meetings.QUOTE_CAP] for ln in lines if key and key in _squash(ln)), None)

        for t in m.get("tasks", []):
            db.add_item(chat_id, "task", title=t["title"], owner=t.get("owner"), unit=t.get("unit"),
                        status=t.get("status", "open"), meeting_id=mid, source_text=quote(t["src"]))
        for d in m.get("decisions", []):
            db.add_item(chat_id, "decision", title=d["title"], status=d.get("status", "open"), meeting_id=mid,
                        source_text=quote(d["src"]))
        for q in m.get("questions", []):
            db.add_item(chat_id, "question", title=q["title"], meeting_id=mid, source_text=quote(q["src"]))
        for p in m.get("proposed", []):
            db.add_item(chat_id, p["kind"], review="proposed", title=p["title"], unit=p.get("unit"), meeting_id=mid,
                        source_text=quote(p["src"]))
    if MEETING_SUMMARY.exists():  # written once by scripts/make_sample_meeting_summary.py with the local model
        s = json.loads(MEETING_SUMMARY.read_text(encoding="utf-8"))
        meeting = db.get_meeting(made[s["key"]])
        db.save_meeting_summary(meeting["id"], s["summary"], meetings.summary_fingerprint(meeting, s["lang"]),
                                s["lang"], s.get("model"), "sample")


def clear_sample() -> int:
    """Delete every sample club and remember not to bring it back."""
    removed = db.delete_samples()
    db.set_meta("sample_dismissed", "1")
    return removed
