"""Club health overview (deterministic) and the AI event planner."""
from __future__ import annotations

from datetime import date, timedelta

from . import db, llm
from .analyzer import _obj, _s, detect_lang, match_member, match_unit, valid_date


def _brief(x: dict) -> dict:
    return {k: x.get(k) for k in ("id", "kind", "title", "owner", "due", "unit", "source_idx")}


def focus(items: list[dict], open_tasks: list[dict], t: str) -> dict:
    """What needs attention today. Categories overlap on purpose (an overdue task can also be ownerless)."""
    by_id = {i["id"]: i for i in items}
    conflicts = []
    for x in items:
        ev = by_id.get(x.get("event_id"))
        if x["kind"] == "task" and x["due"] and ev and ev["due"] and x["due"] > ev["due"]:
            conflicts.append({**_brief(x), "why": "after_event", "event": ev["title"], "event_date": ev["due"]})
        if x["kind"] == "event" and x["due"]:
            if x["phase"] == "held" and x["due"] > t:
                conflicts.append({**_brief(x), "why": "held_in_future"})
            elif x["phase"] in ("planning", "confirmed") and x["due"] < t:
                conflicts.append({**_brief(x), "why": "past_not_held"})
    return {
        "overdue": [_brief(x) for x in open_tasks if x["due"] and x["due"] < t],
        "orphans": [_brief(x) for x in open_tasks if not x["owner"]],
        "conflicts": conflicts,
        # decisions the club has not marked final yet
        "decisions": [_brief(x) for x in items if x["kind"] == "decision" and x["status"] == "open" and x["validity"] == "valid"],
    }


def upcoming_events(items: list[dict], t: str) -> list[dict]:
    today = date.fromisoformat(t)
    out = []
    for e in sorted((e for e in items if e["kind"] == "event" and e["due"] and e["due"] >= t
                     and e["phase"] not in ("cancelled", "held")), key=lambda e: e["due"]):
        linked = [x for x in items if x["kind"] == "task" and x.get("event_id") == e["id"]]
        out.append({"id": e["id"], "title": e["title"], "date": e["due"], "time": e["time"], "place": e["place"],
                    "phase": e["phase"], "days": (date.fromisoformat(e["due"]) - today).days,
                    "open_tasks": sum(1 for x in linked if x["status"] == "open"), "tasks": len(linked)})
    return out[:5]


def overview(chat: dict, items: list[dict], members: list[str], today: date) -> dict:
    t = today.isoformat()
    week = (today + timedelta(days=7)).isoformat()
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
        "focus": focus(items, open_, t),
        "events": upcoming_events(items, t),
        "kpi": {"upcoming_ids": [x["id"] for x in open_ if x["due"] and t <= x["due"] <= week],
                "questions_total": sum(1 for q in items if q["kind"] == "question"),
                "dated": sum(1 for x in tasks if x["due"]),
                "open": len(open_), "done": len(tasks) - len(open_), "total": len(tasks),
                "questions": sum(1 for q in items if q["kind"] == "question" and q["status"] == "open"),
                "orphans": sum(1 for x in open_ if not x["owner"]),
                "decisions": sum(1 for d in items if d["kind"] == "decision" and d["validity"] == "valid"),
                "next_event": ({"title": events[0]["title"], "date": events[0]["due"], "time": events[0]["time"],
                                "days": (date.fromisoformat(events[0]["due"]) - today).days} if events else None)},
        "units": units, "workload": workload, "alerts": alerts, "timeline": timeline,
    }


PLAN_SCHEMA = _obj(
    title=_s,
    event_date=_s,
    tasks={"type": "array", "items": _obj(title=_s, unit=_s, owner=_s, due=_s, why=_s)},
    meetings={"type": "array", "items": _obj(title=_s, units={"type": "array", "items": _s}, date=_s, agenda=_s)},
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
request. For every task also give "why": one short sentence on why it comes at that point in the order (what it
unblocks or depends on). List tasks in the order they must be done.
Also propose 2 to 4 preparation meetings: which teams (from the list) must meet, on which date (before the event,
after the tasks they depend on are under way), and a one-sentence agenda. Do not invent teams.
Write titles in {'Turkish' if lang == 'tr' else 'English'}, max 6 words per title; write why and agenda in the same language."""
    r = await llm.chat_json([{"role": "user", "content": prompt}], PLAN_SCHEMA, temperature=0.3)
    event_date = valid_date(r.get("event_date", ""), today)
    tasks = []
    for t in r.get("tasks", []):
        if not (t.get("title") or "").strip():
            continue
        owner = match_member(t.get("owner", ""), members)
        tasks.append({"title": t["title"].strip(), "unit": match_unit(t.get("unit", ""), chat["units"]),
                      "owner": owner if owner in members else None,
                      "due": valid_date(t.get("due", ""), today), "why": (t.get("why") or "").strip()})
    follow = ("rapor", "anket", "teşekkür", "geri bildirim", "survey", "report", "thank", "feedback", "follow")
    if event_date:
        for x in tasks:  # preparation can't happen after the event itself
            if x["due"] and x["due"] > event_date and not any(w in x["title"].lower() for w in follow):
                x["due"] = (date.fromisoformat(event_date) - timedelta(days=1)).isoformat()
    tasks.sort(key=lambda x: x["due"] or "9999")
    meets = []
    for m in r.get("meetings", []):
        units = [u for u in dict.fromkeys(match_unit(u, chat["units"]) for u in m.get("units", [])) if u]
        d = valid_date(m.get("date", ""), today)
        if (m.get("title") or "").strip() and units and (not event_date or not d or d <= event_date):
            meets.append({"title": m["title"].strip(), "units": units, "date": d, "agenda": (m.get("agenda") or "").strip()})
    meets.sort(key=lambda x: x["date"] or "9999")
    plan = {"title": (r.get("title") or goal).strip(), "event_date": event_date, "tasks": tasks, "meetings": meets,
            "model": llm.MODEL}
    plan["saved_id"] = db.save_ai(chat_id, "plan", plan["title"], {**plan, "goal": goal}, llm.MODEL)
    return plan


IDEAS_SCHEMA = _obj(ideas={"type": "array", "items": _obj(title=_s, why=_s, based_on=_s, unit=_s)})


def _past_events_text(events: list[dict]) -> str:
    def v(x):
        return "-" if x in (None, "", []) else x
    return "\n".join(
        f"- {e['title']} | type: {v(e['event_type'])} | {v(e['due'])} | teams: {v(', '.join(e['event_units']))} | "
        f"attendance {v(e['attendees_actual'])}/{v(e['attendees_expected'])} | score {v(e['feedback_score'])} | "
        f"went well: {v(e.get('feedback_good'))} | fell short: {v(e.get('feedback_bad'))}" for e in events)


async def suggest_events(chat_id: int, today: date) -> dict:
    """New event ideas drawn from the club's own held events. Each idea must point at a recorded event (`based_on`);
    an idea whose reference is not a recorded event title is dropped, so nothing rests on invented history."""
    chat = db.get_chat(chat_id)
    items = db.get_items(chat_id)
    held = [e for e in items if e["kind"] == "event" and e["phase"] == "held"]
    if not held:
        return {"ideas": [], "reason": "no_held_events"}
    lang = detect_lang(db.get_messages(chat_id)[:200])
    decisions = [d["title"] for d in items if d["kind"] == "decision" and d["validity"] == "valid"][:10]
    planned = [e["title"] for e in items if e["kind"] == "event" and e["phase"] in ("idea", "planning", "confirmed")]
    prompt = f"""You advise a student club on its next events. Today is {today:%Y-%m-%d}.
Club: {chat['name']}. Teams: {', '.join(chat['units'])}.
HELD EVENTS (the only history you may rely on):
{_past_events_text(held)}
Valid club decisions: {'; '.join(decisions) or '-'}
Already planned (do not repeat): {'; '.join(planned) or '-'}

Suggest 3 new event ideas that fit this club's style and build on what worked: repeat what scored and attended well,
fix what fell short, and vary the format. For each: title (max 7 words), why (one sentence citing the recorded
attendance, score or feedback that supports it; use only figures written above), based_on (copy ONE held event
title exactly from the list), unit (one of the teams, "" if unsure). Write in {'Turkish' if lang == 'tr' else 'English'}."""
    r = await llm.chat_json([{"role": "user", "content": prompt}], IDEAS_SCHEMA, temperature=0.5)
    titles = {e["title"].strip().casefold(): e["title"] for e in held}
    ideas = []
    for x in r.get("ideas", []):
        ref = titles.get((x.get("based_on") or "").strip().casefold())
        if not (x.get("title") or "").strip() or not ref:
            continue
        ideas.append({"title": x["title"].strip(), "why": (x.get("why") or "").strip(), "based_on": ref,
                      "unit": match_unit(x.get("unit", ""), chat["units"])})
    out = {"ideas": ideas[:3], "model": llm.MODEL}
    if out["ideas"]:
        out["saved_id"] = db.save_ai(chat_id, "ideas", f"{today:%Y-%m-%d} · {len(out['ideas'])}", out, llm.MODEL)
    return out
