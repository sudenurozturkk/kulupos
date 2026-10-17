"""Club health overview (deterministic) and the AI event planner."""
from __future__ import annotations

from datetime import date, timedelta

from . import db, llm
from .analyzer import _obj, _s, detect_lang, match_member, match_unit, valid_date


def overview(chat: dict, items: list[dict], members: list[str], today: date) -> dict:
    t = today.isoformat()
    soon = (today + timedelta(days=3)).isoformat()
    tasks = [i for i in items if i["kind"] == "task"]
    open_ = [x for x in tasks if x["status"] == "open"]

    units = []
    for u in [*chat["units"], None]:
        mine = [x for x in tasks if (x["unit"] if x["unit"] in chat["units"] else None) == u]
        if u is None and not mine:
            continue
        o = [x for x in mine if x["status"] == "open"]
        overdue = [x for x in o if x["due"] and x["due"] < t]
        orphans = [x for x in o if not x["owner"]]
        health = "bad" if overdue else "warn" if orphans or any(x["due"] and x["due"] <= soon for x in o) else "ok"
        if not mine:
            health = "idle"
        units.append({"name": u, "total": len(mine), "done": len(mine) - len(o), "open": len(o),
                      "overdue": len(overdue), "orphans": len(orphans), "health": health})

    workload = sorted(({"name": m, "open": sum(1 for x in open_ if x["owner"] == m),
                        "done": sum(1 for x in tasks if x["owner"] == m and x["status"] == "done")}
                       for m in members), key=lambda w: (-w["open"], -w["done"]))
    workload = [w for w in workload if w["open"] or w["done"]]

    events = sorted((e for e in items if e["kind"] == "event" and e["due"] and e["due"] >= t
                           and e["phase"] not in ("cancelled", "held")),
                    key=lambda e: e["due"])
    alerts = []
    for e in events[:2]:
        days = (date.fromisoformat(e["due"]) - today).days
        before = [x for x in open_ if not x["due"] or x["due"] <= e["due"]]
        orphan_n = sum(1 for x in before if not x["owner"])
        alerts.append({"level": "bad" if days <= 7 and (orphan_n or before) else "warn",
                       "type": "event", "event": e["title"], "days": days,
                       "open": len(before), "orphans": orphan_n})
    for x in open_:
        if x["due"] and x["due"] < t:
            alerts.append({"level": "bad", "type": "overdue", "title": x["title"], "owner": x["owner"], "due": x["due"]})
    for q in items:
        if q["kind"] == "question" and q["status"] == "open":
            alerts.append({"level": "warn", "type": "question", "title": q["title"], "owner": q["owner"]})
    overloaded = [w for w in workload if w["open"] >= 3]
    for w in overloaded:
        alerts.append({"level": "warn", "type": "load", "owner": w["name"], "open": w["open"]})

    timeline = sorted(
        [{"date": x["due"], "title": x["title"], "kind": x["kind"], "owner": x["owner"], "id": x["id"],
          "status": x["status"]}
         for x in items if x["due"] and x["due"] >= t and x["kind"] in ("task", "event") and x["status"] == "open"
         and x["phase"] not in ("cancelled", "held")],
        key=lambda r: r["date"])[:10]

    return {
        "kpi": {"open": len(open_), "done": len(tasks) - len(open_), "total": len(tasks),
                "questions": sum(1 for q in items if q["kind"] == "question" and q["status"] == "open"),
                "orphans": sum(1 for x in open_ if not x["owner"]),
                "decisions": sum(1 for d in items if d["kind"] == "decision"),
                "next_event": ({"title": events[0]["title"], "date": events[0]["due"], "time": events[0]["time"],
                                "days": (date.fromisoformat(events[0]["due"]) - today).days} if events else None)},
        "units": units, "workload": workload, "alerts": alerts, "timeline": timeline,
    }


PLAN_SCHEMA = _obj(
    title=_s,
    event_date=_s,
    tasks={"type": "array", "items": _obj(title=_s, unit=_s, owner=_s, due=_s)},
)


async def plan_event(chat_id: int, goal: str, today: date) -> dict:
    chat = db.get_chat(chat_id)
    members = db.senders(chat_id)
    items = db.get_items(chat_id)
    lang = detect_lang(db.get_messages(chat_id)[:200])
    load = {m: sum(1 for x in items if x["kind"] == "task" and x["status"] == "open" and x["owner"] == m)
            for m in members}
    done_by = {}
    for x in items:
        if x["kind"] == "task" and x["owner"] and x["unit"]:
            done_by.setdefault(x["owner"], set()).add(x["unit"])
    roster = "\n".join(f"- {m}: open tasks {load[m]}; has worked on {', '.join(sorted(done_by.get(m, []))) or '-'}"
                       for m in members)
    cal = ", ".join(f"{(today + timedelta(n)):%a %Y-%m-%d}" for n in range(0, 70, 1))
    prompt = f"""You plan events for a student club. Today is {today:%A %Y-%m-%d}.
Club units: {', '.join(chat['units'])}
Members (with current load and the units they already worked in):
{roster}
CALENDAR: {cal}

Request: {goal}

Produce a realistic preparation plan: 8 to 10 concrete tasks covering venue/permits, speakers or content,
sponsorship, promotion, registration, logistics/tech, the event day and the follow-up. For each task pick the
unit from the list, suggest an owner from the members (prefer people who already worked in that unit and have
fewer open tasks; "" if nobody fits), and a due date YYYY-MM-DD scheduled backwards from the event date
(permits and venue first, promotion 1-2 weeks before). Every due date must be on or before event_date, except
at most one follow-up task (survey, report, thank-you) after it. event_date = the event date resolved from the
request. Write titles in {'Turkish' if lang == 'tr' else 'English'}, max 6 words per title."""
    r = await llm.chat_json([{"role": "user", "content": prompt}], PLAN_SCHEMA, temperature=0.3)
    event_date = valid_date(r.get("event_date", ""), today)
    tasks = []
    for t in r.get("tasks", []):
        if not (t.get("title") or "").strip():
            continue
        owner = match_member(t.get("owner", ""), members)
        tasks.append({"title": t["title"].strip(), "unit": match_unit(t.get("unit", ""), chat["units"]),
                      "owner": owner if owner in members else None,
                      "due": valid_date(t.get("due", ""), today), "why": ""})
    follow = ("rapor", "anket", "teşekkür", "geri bildirim", "survey", "report", "thank", "feedback", "follow")
    if event_date:
        for x in tasks:  # preparation can't happen after the event itself
            if x["due"] and x["due"] > event_date and not any(w in x["title"].lower() for w in follow):
                x["due"] = (date.fromisoformat(event_date) - timedelta(days=1)).isoformat()
    tasks.sort(key=lambda x: x["due"] or "9999")
    return {"title": (r.get("title") or goal).strip(), "event_date": event_date, "tasks": tasks}
