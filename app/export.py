"""File exports of approved records only: CSV/JSON for tasks, decisions, open questions; Markdown analysis summary."""
from __future__ import annotations

import csv
import io
import json
from datetime import date

from . import db
from .analyzer import detect_lang

KINDS = {"tasks": "task", "decisions": "decision", "questions": "question"}
COLUMNS = ["id", "title", "owner", "unit", "due", "status", "source_idx", "source_sender", "source_date", "source_text"]
UNSAFE = ("=", "+", "-", "@", "\t", "\r")


def safe_cell(v) -> str:
    """Spreadsheet formula injection guard: text from the chat or the user must never start a formula."""
    s = "" if v is None else str(v)
    return "'" + s if s.startswith(UNSAFE) else s


class FilterError(ValueError):
    pass


def _day(v: str | None, name: str) -> str | None:
    if not v:
        return None
    try:
        return date.fromisoformat(v).isoformat()
    except ValueError:
        raise FilterError(f"{name}: YYYY-MM-DD")


def rows_for(chat_id: int, what: str, status: str | None, owner: str | None, unit: str | None,
             date_from: str | None, date_to: str | None) -> tuple[list[dict], dict]:
    """Approved rows of one kind + the filters that were applied (written into the file)."""
    if what not in KINDS:
        raise FilterError("what: tasks | decisions | questions")
    date_from, date_to = _day(date_from, "date_from"), _day(date_to, "date_to")
    if date_from and date_to and date_from > date_to:
        raise FilterError("date_from > date_to")
    status = status or ("open" if what == "questions" else "all")
    if status not in ("all", "open", "done", "answered", "resolved", "invalid"):
        raise FilterError("status: all | open | done | answered | resolved | invalid")
    msgs = {m["idx"]: m for m in db.get_messages(chat_id)}
    out = []
    for i in db.get_items(chat_id, kind=KINDS[what]):
        m = msgs.get(i["source_idx"]) if i["source_idx"] is not None else None
        # the date a range applies to: due date for tasks, source message date for decisions/questions
        day = i["due"] if what == "tasks" else (m["ts"][:10] if m else None)
        if status != "all" and i["status"] != status:
            continue
        if owner and (i["owner"] or "") != owner:
            continue
        if unit and (i["unit"] or "") != unit:
            continue
        if (date_from or date_to) and (not day or (date_from and day < date_from) or (date_to and day > date_to)):
            continue
        out.append({"id": i["id"], "title": i["title"], "owner": i["owner"] or "", "unit": i["unit"] or "",
                    "due": i["due"] or "", "status": i["status"],
                    "source_idx": i["source_idx"] if i["source_idx"] is not None else "",
                    "source_sender": (m["sender"] or "") if m else "", "source_date": m["ts"] if m else "",
                    "source_text": m["text"] if m else ""})
    filters = {"what": what, "status": status, "owner": owner or "all", "unit": unit or "all",
               "date_field": "due" if what == "tasks" else "source_date",
               "date_from": date_from or "-", "date_to": date_to or "-"}
    return out, filters


def _filter_line(f: dict) -> str:
    return ("filters: " + ", ".join(f"{k}={f[k]}" for k in
            ("status", "owner", "unit", "date_field", "date_from", "date_to"))
            + " | only approved records; source_text is the original message (a leading = + - @ is prefixed with ')")


def to_csv(rows: list[dict], filters: dict, today: str) -> str:
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\r\n")
    w.writerow([f"# Pano export {filters['what']} {today}"])
    w.writerow([_filter_line(filters)])
    w.writerow(COLUMNS)
    for r in rows:
        w.writerow([r[c] if c == "id" else safe_cell(r[c]) for c in COLUMNS])
    return "﻿" + buf.getvalue()  # BOM so Excel reads Turkish characters


def to_json(rows: list[dict], filters: dict, today: str) -> str:
    return json.dumps({"exported": today, "filters": filters, "only_approved": True, "count": len(rows),
                       "rows": rows}, ensure_ascii=False, indent=2)


L = {"tr": dict(title="Analiz özeti", filt="Filtre", period="Mesaj aralığı", counts="Sayılar (yalnızca onaylı kayıtlar)",
                tasks="Görevler", open="açık", done="tamamlandı", decisions="Kararlar", questions="Açık sorular",
                units="Birim bazında açık görev", none="Yok", pending="Onay bekleyen AI önerisi",
                note="Bu özet yalnızca onaylanmış kayıtlardan üretildi; onay bekleyenler dahil değildir."),
     "en": dict(title="Analysis summary", filt="Filter", period="Message range", counts="Counts (approved records only)",
                tasks="Tasks", open="open", done="done", decisions="Decisions", questions="Open questions",
                units="Open tasks per unit", none="None", pending="AI suggestions awaiting approval",
                note="Built from approved records only; pending suggestions are not included.")}


def summary_md(chat_id: int, status: str | None, owner: str | None, unit: str | None,
               date_from: str | None, date_to: str | None, today: str) -> str:
    chat = db.get_chat(chat_id)
    lang = detect_lang(db.get_messages(chat_id))
    s = L[lang]
    data = {}
    for what in KINDS:
        data[what], _ = rows_for(chat_id, what, status if what == "tasks" else None, owner, unit, date_from, date_to)
    tasks = data["tasks"]
    first, last = (chat.get("first_ts") or "-")[:10], (chat.get("last_ts") or "-")[:10]
    flt = ", ".join(f"{k}={v}" for k, v in (("status(tasks)", status or "all"), ("owner", owner or "all"),
                                            ("unit", unit or "all"), ("date_from", date_from or "-"),
                                            ("date_to", date_to or "-")))
    out = [f"# {chat['name']} — {s['title']}", "", f"_Pano · {today}_", "",
           f"- **{s['period']}:** {first} – {last}",
           f"- **{s['filt']}:** {flt} (date: tasks→due, others→source date)",
           f"- {s['note']}", "", f"## {s['counts']}", "",
           f"- {s['tasks']}: {len(tasks)} ({sum(t['status'] == 'open' for t in tasks)} {s['open']}, "
           f"{sum(t['status'] == 'done' for t in tasks)} {s['done']})",
           f"- {s['decisions']}: {len(data['decisions'])}",
           f"- {s['questions']}: {len(data['questions'])}",
           f"- {s['pending']}: {len(db.get_items(chat_id, review='proposed'))}", ""]
    per_unit: dict[str, int] = {}
    for t in tasks:
        if t["status"] == "open":
            u = t["unit"] or "—"
            per_unit[u] = per_unit.get(u, 0) + 1
    out += [f"## {s['units']}", ""] + ([f"- {u}: {n}" for u, n in sorted(per_unit.items())] or [f"- {s['none']}"]) + [""]
    for key in ("decisions", "questions"):
        out += [f"## {s[key]}", ""]
        out += [f"- {r['title']}" + (f" (msg #{r['source_idx']})" if r["source_idx"] != "" else "")
                for r in data[key]] or [f"- {s['none']}"]
        out.append("")
    return "\n".join(out)
