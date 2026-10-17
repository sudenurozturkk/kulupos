"""People derived from the records: task owners. No table, no accounts, no judgement - only counts and the lists
behind them. Names are matched exactly (case/space-insensitive); nothing is guessed."""
from __future__ import annotations

import re


def key(name: str | None) -> str:
    return " ".join((name or "").casefold().split())


def _listed(text: str | None, name: str) -> bool:
    """`name` appears as a whole entry of a free-text, comma/newline separated list."""
    return any(key(x) == key(name) for x in re.split(r"[,\n;]", text or ""))


def names(items: list[dict]) -> list[str]:
    """Owners of approved tasks, spelled as first seen; sorted."""
    seen: dict[str, str] = {}
    for i in items:
        if i["kind"] == "task" and i["owner"] and key(i["owner"]) not in seen:
            seen[key(i["owner"])] = i["owner"]
    return sorted(seen.values(), key=str.casefold)


def _mine(items: list[dict], name: str) -> list[dict]:
    return [i for i in items if i["kind"] == "task" and key(i["owner"]) == key(name)]


def summary(items: list[dict], chat: dict, today: str) -> list[dict]:
    out = []
    for n in names(items):
        t = _mine(items, n)
        out.append({"name": n, "committees": committees(t, chat, n),
                    "open": sum(1 for x in t if x["status"] == "open"),
                    "late": sum(1 for x in t if x["status"] == "open" and x["due"] and x["due"] < today),
                    "done": sum(1 for x in t if x["status"] == "done")})
    return out


def committees(tasks: list[dict], chat: dict, name: str) -> list[str]:
    """Committees whose member list names the person, plus the committees of their tasks."""
    found = [u for u, members in chat["unit_members"].items() if _listed(members, name)]
    found += [t["unit"] for t in tasks if t["unit"]]
    return list(dict.fromkeys(found))


def detail(items: list[dict], chat: dict, meetings: list[dict], name: str, today: str) -> dict:
    tasks = _mine(items, name)
    events = {i["id"]: i for i in items if i["kind"] == "event"}
    linked = {t["event_id"] for t in tasks if t["event_id"] in events}
    owned = {i["id"] for i in events.values() if key(i["owner"]) == key(name)}
    open_ = [t for t in tasks if t["status"] == "open"]
    late = [t for t in open_ if t["due"] and t["due"] < today]
    return {
        "name": name, "today": today,
        "committees": committees(tasks, chat, name),
        "open": [t for t in open_ if t not in late],
        "late": late,
        "done": [t for t in tasks if t["status"] == "done"],
        "upcoming": sorted((t for t in open_ if t["due"] and t["due"] >= today), key=lambda t: t["due"]),
        "events": [{"id": e["id"], "title": e["title"], "due": e["due"], "phase": e["phase"],
                    "role": [r for r, ok in (("owner", e["id"] in owned), ("task", e["id"] in linked)) if ok]}
                   for e in (events[i] for i in sorted(owned | linked))],
        "meetings": [{"id": m["id"], "title": m["title"], "date": m["date"], "status": m["status"]}
                     for m in meetings if _listed(m["attendees"], name)],
    }
