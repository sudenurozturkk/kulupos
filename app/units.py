"""Committee page data and the AI committee report (written only from the committee's own records)."""
from __future__ import annotations

from datetime import date

from . import db, llm, report


def page(chat_id: int, unit: str, today: str) -> dict:
    chat = db.get_chat(chat_id)
    items = db.get_items(chat_id)
    events = [e for e in items if e["kind"] == "event" and unit in (e["event_units"] or [])]
    ev_by_id = {e["id"]: e for e in items if e["kind"] == "event"}
    tasks = [t for t in items if t["kind"] == "task" and t["unit"] == unit]
    meetings = [m for m in db.get_meetings(chat_id) if unit in (m["units"] or [])]
    members = [x.strip() for x in (chat["unit_members"].get(unit) or "").split(",") if x.strip()]
    owners = sorted({t["owner"] for t in tasks if t["owner"]})
    open_ = [t for t in tasks if t["status"] != "done"]
    late = [t for t in open_ if t["due"] and t["due"] < today]
    return {"unit": unit, "members": members, "owners": owners, "today": today,
            "tasks": tasks, "open": len(open_), "done": len(tasks) - len(open_), "late": len(late),
            "orphans": len([t for t in open_ if not t["owner"]]),
            "events": events, "meetings": meetings,
            "decisions": [d for d in items if d["kind"] == "decision" and d["event_id"] in {e["id"] for e in events} and d["validity"] == "valid"],
            "event_of": {t["id"]: (ev_by_id[t["event_id"]]["title"] if t["event_id"] in ev_by_id else None) for t in tasks}}


def facts_text(chat_id: int, unit: str, today: str) -> str:
    p = page(chat_id, unit, today)

    def v(x):
        return "-" if x in (None, "", []) else str(x)
    lines = [f"COMMITTEE: {unit}", f"Today: {today}", f"Members: {v(', '.join(p['members']))}",
             f"Tasks: {len(p['tasks'])} total, {p['done']} done, {p['open']} open, {p['late']} overdue, {p['orphans']} open without owner", "TASKS:"]
    lines += [f"- [{t['status']}] {t['title']} | owner {v(t['owner'])} | due {v(t['due'])} | event {v(p['event_of'].get(t['id']))}" for t in p["tasks"]] or ["(none)"]
    lines.append("EVENTS THE COMMITTEE TOOK PART IN:")
    for e in p["events"]:
        fb = " ".join(x for x in (e.get("feedback_note"), e.get("feedback_good"), e.get("feedback_bad")) if x)
        lines.append(f"- {e['title']} | {v(e['phase'])} | {v(e['due'])} | expected {v(e['attendees_expected'])} | actual {v(e['attendees_actual'])} | "
                     f"budget plan {v(e['budget_est'])} | actual {v(e['budget_actual'])} | score {v(e['feedback_score'])} | feedback {v(fb)}")
    if not p["events"]:
        lines.append("(none)")
    lines.append("MEETINGS:")
    lines += [f"- {m['title']} | {v(m['date'])} | {m['status']}" for m in p["meetings"]] or ["(none)"]
    return "\n".join(lines)


async def generate(chat_id: int, unit: str, today: str, lang: str = "tr") -> dict:
    facts = facts_text(chat_id, unit, today)
    language = "Turkish" if lang == "tr" else "English"
    system = (f"You write a short, useful committee report for a student club lead, in {language}. Use ONLY the recorded data. "
              f"Plain text with these headings: Durum (status), Güçlü yönler (strengths), Dikkat edilecekler (risks), Öneriler "
              f"(2-4 concrete suggestions for the next weeks). Name people and events only as they appear in the data. Never invent "
              f"numbers, dates or names; do not compute percentages. No emojis. If a part has no data, skip it.")
    msgs = [{"role": "system", "content": system}, {"role": "user", "content": f"RECORDED DATA:\n{facts}\n\nWrite the report."}]
    text = (await llm.chat(msgs, temperature=0.3)).strip()
    bad = report.unsupported_figures(text, facts)
    if bad:
        msgs[1]["content"] += f"\nYour previous draft used figures that are not in the data: {', '.join(bad)}. Remove them."
        text = (await llm.chat(msgs, temperature=0.0)).strip()
        bad = report.unsupported_figures(text, facts)
        if bad:
            raise report.ReportRejected(bad)
    return {"report": text, "fingerprint": report.fingerprint(facts), "model": llm.MODEL}


def view(chat_id: int, unit: str, today: str, lang: str = "tr") -> dict:
    row = db.get_unit_report(chat_id, unit)
    fp = report.fingerprint(facts_text(chat_id, unit, today))
    return {"report": row["body"] if row else None, "model": row["model"] if row else None,
            "created_at": row["created_at"] if row else None, "stale": bool(row and row["fingerprint"] != fp)}
