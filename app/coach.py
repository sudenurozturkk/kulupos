"""Two Gemma helpers built only from the club's own records: the week plan (what to do first, in order) and the
handover report (what the next board needs to know). Both are saved (ai_saved) and can be deleted."""
from __future__ import annotations

import re
from datetime import date, timedelta

from . import db, llm, meetings, report
from .analyzer import _obj, _s, detect_lang, match_member, match_unit, valid_date

WEEK_SCHEMA = _obj(assessment=_s, steps={"type": "array", "items": _obj(action=_s, why=_s, ref=_s, unit=_s, owner=_s, when=_s)},
                   agenda={"type": "array", "items": _s})
HORIZON = 30


_TOKEN = re.compile(r"\[([TEQDM])(\d+)\]")
_BARE = re.compile(r"\s*\(\s*[TEQDM]\d+\s*\)")


def titles_by_ref(chat_id: int) -> dict[str, str]:
    refs = {f"{i['kind'][0].upper() if i['kind'] != 'task' else 'T'}{i['id']}": i["title"] for i in db.get_items(chat_id)}
    refs.update({f"M{m['id']}": m["title"] for m in db.get_meetings(chat_id)})
    return refs


def clean_ids(text: str, refs: dict[str, str] | None = None) -> str:
    """Record ids like [T18] are for the model, not for readers: show the record's title instead (unknown ids vanish)."""
    refs = refs or {}
    text = _BARE.sub("", text or "")
    text = _TOKEN.sub(lambda m: f"“{refs[m.group(1) + m.group(2)]}”" if m.group(1) + m.group(2) in refs else "", text)
    return re.sub(r"\(\s*\)", "", text).replace(" ,", ",").replace(" .", ".").replace("  ", " ").strip()


def clean_week(w: dict, refs: dict[str, str] | None = None) -> dict:
    for s in w.get("steps", []):
        s["action"], s["why"] = clean_ids(s["action"], refs), clean_ids(s["why"], refs)
    w["assessment"] = clean_ids(w.get("assessment", ""), refs)
    w["agenda"] = [clean_ids(a, refs) for a in w.get("agenda", [])]
    return w


def _v(x):
    return "-" if x in (None, "", []) else x


def week_facts(chat_id: int, today: date) -> tuple[str, set[str], list[str]]:
    """Records with short ids (T=task, E=event, Q=question, D=decision, M=meeting) so a step can point at one."""
    chat, items = db.get_chat(chat_id), db.get_items(chat_id)
    t, soon = today.isoformat(), (today + timedelta(days=HORIZON)).isoformat()
    tasks = [i for i in items if i["kind"] == "task" and i["status"] != "done"]
    members = db.senders(chat_id)
    ids: set[str] = set()

    def line(prefix, x, extra=""):
        ids.add(f"{prefix}{x['id']}")
        return (f"- [{prefix}{x['id']}] {x['title']} | owner: {_v(x['owner'])} | due: {_v(x['due'])} | "
                f"team: {_v(x['unit'])}{extra}")

    overdue = [line("T", x) for x in tasks if x["due"] and x["due"] < t]
    orphans = [line("T", x) for x in tasks if not x["owner"]]
    events = []
    for e in items:
        if e["kind"] == "event" and e["phase"] in ("idea", "planning", "confirmed") and (not e["due"] or e["due"] <= soon):
            linked = [x for x in tasks if x["event_id"] == e["id"]]
            events.append(line("E", e, f" | open linked tasks: {len(linked)}, without owner: "
                                       f"{sum(1 for x in linked if not x['owner'])}"))
    questions = [line("Q", x) for x in items if x["kind"] == "question" and x["status"] == "open"]
    decisions = [line("D", x) for x in items if x["kind"] == "decision" and x["status"] == "open" and x["validity"] == "valid"]
    planned = []
    for m in db.get_meetings(chat_id):
        if m["status"] == "planned":
            ids.add(f"M{m['id']}")
            planned.append(f"- [M{m['id']}] {m['title']} | date: {_v(m['date'])} | teams: {_v(', '.join(m['units']))}")
    none = ["(none)"]
    lines = [f"CLUB: {chat['name']} | teams: {', '.join(chat['units'])} | today: {t}", "",
             "OVERDUE TASKS:", *(overdue or none), "OPEN TASKS WITHOUT OWNER:", *(orphans or none),
             "UPCOMING EVENTS (next 30 days):", *(events or none), "OPEN QUESTIONS:", *(questions or none),
             "OPEN DECISIONS:", *(decisions or none), "PLANNED MEETINGS:", *(planned or none),
             "OPEN TASKS PER TEAM:", *[f"- {u}: {sum(1 for x in tasks if x['unit'] == u)}" for u in chat["units"]],
             "OPEN TASKS PER MEMBER:", *[f"- {m}: {sum(1 for x in tasks if x['owner'] == m)}" for m in members]]
    return "\n".join(lines), ids, members


async def week_plan(chat_id: int, today: date) -> dict:
    chat = db.get_chat(chat_id)
    facts, ids, members = week_facts(chat_id, today)
    if not ids:
        return {"steps": [], "reason": "nothing_open"}
    lang = detect_lang(db.get_messages(chat_id)[:200])
    cal = ", ".join(f"{(today + timedelta(n)):%a %Y-%m-%d}" for n in range(0, 14))
    prompt = f"""You are the planning assistant of a student club. Use ONLY the records below.
{facts}
CALENDAR: {cal}

Write the club's plan for the next 7 days: 4 to 7 steps in the order they should be done (overdue work and events that are
close come first; ownerless work before things that already have an owner). Each step: action (max 12 words, an
instruction), why (one sentence naming the record that makes it urgent, with its figures as written above),
ref (the id in brackets of the record it is about, e.g. T12; "" when it concerns a whole team), unit (one of the teams,
"" if unsure), owner (a member from the lists only, preferring those with fewer open tasks; "" if nobody fits), when
(YYYY-MM-DD from the calendar). If a team has many open tasks or a planned meeting is due, you may propose that the team
meet. Also write assessment: 3 or 4 sentences that judge the club's current state for its board (what is going
well, what is the biggest risk, what to do about it), quoting only figures that are written above, and agenda: 4 to 6
short items for this week's board meeting that follow from the steps. Never invent records, people, teams or dates. Write in {'Turkish' if lang == 'tr' else 'English'}."""
    r = await llm.chat_json([{"role": "user", "content": prompt}], WEEK_SCHEMA, temperature=0.3)
    steps = []
    for x in r.get("steps", []):
        ref = "".join(ch for ch in (x.get("ref") or "").upper() if ch.isalnum())   # "[T12]" -> "T12"
        unit = match_unit(x.get("unit", ""), chat["units"])
        if not (x.get("action") or "").strip() or not (ref in ids or (not ref and unit)):
            continue   # a step must point at a real record or at a real team
        owner = match_member(x.get("owner", ""), members)
        steps.append({"action": x["action"].strip(), "why": (x.get("why") or "").strip(), "ref": ref or None,
                      "unit": unit, "owner": owner if owner in members else None,
                      "when": valid_date(x.get("when", ""), today)})
    steps.sort(key=lambda s: s["when"] or "9999")
    assessment = (r.get("assessment") or "").strip()
    if report.unsupported_figures(assessment, facts):
        assessment = ""   # a figure that is not in the records: leave the judgement out rather than show it
    agenda = [a.strip() for a in r.get("agenda", []) if a and a.strip() and not report.unsupported_figures(a, facts)][:6]
    out = {"steps": steps[:7], "assessment": assessment, "agenda": agenda, "model": llm.MODEL, "date": today.isoformat()}
    clean_week(out, titles_by_ref(chat_id))
    if out["steps"]:
        out["saved_id"] = db.save_ai(chat_id, "week", f"{today:%Y-%m-%d} · {len(out['steps'])}", out, llm.MODEL)
    return out


# ---- handover report ---------------------------------------------------------------------------

HANDOVER_SECTIONS = {"tr": "Genel görünüm, Yapılan etkinlikler, Alınan kararlar, Devredilen açık işler, "
                           "Geri bildirimlerden öğrenilenler, Yeni yönetime öneriler",
                     "en": "Overview, Events held, Decisions, Open work handed over, Lessons from feedback, "
                           "Suggestions for the next board"}


def handover_facts(chat_id: int) -> str:
    chat, items = db.get_chat(chat_id), db.get_items(chat_id)
    tasks = [i for i in items if i["kind"] == "task"]
    done = [x for x in tasks if x["status"] == "done"]
    held = [e for e in items if e["kind"] == "event" and e["phase"] == "held"]
    none = ["(none)"]
    ev = [f"- {e['title']} | {_v(e['due'])} | attendance {_v(e['attendees_actual'])}/{_v(e['attendees_expected'])}"
          f" | budget {_v(e['budget_actual'])}/{_v(e['budget_est'])} | score {_v(e['feedback_score'])}"
          f" | went well: {report._clean(e.get('feedback_good') or '-')} | fell short: {report._clean(e.get('feedback_bad') or '-')}"
          for e in held]
    lines = [f"CLUB: {chat['name']}", f"Teams: {', '.join(chat['units'])}",
             f"Tasks: total {len(tasks)}, done {len(done)}, open {len(tasks) - len(done)}", "TASKS PER TEAM (done/open):",
             *[f"- {u}: {sum(1 for x in done if x['unit'] == u)}/"
               f"{sum(1 for x in tasks if x['unit'] == u and x['status'] != 'done')}" for u in chat["units"]],
             "", "EVENTS HELD:", *(ev or none),
             "VALID DECISIONS:", *([f"- {d['title']}" for d in items if d["kind"] == "decision" and d["validity"] == "valid"] or none),
             "OPEN TASKS TO HAND OVER:",
             *([f"- {x['title']} | owner: {_v(x['owner'])} | due: {_v(x['due'])}" for x in tasks if x["status"] != "done"] or none),
             "OPEN QUESTIONS:", *([f"- {q['title']}" for q in items if q["kind"] == "question" and q["status"] == "open"] or none),
             "MEETINGS:", *([f"- {m['title']} | {_v(m['date'])} | {m['status']}" for m in db.get_meetings(chat_id)] or none)]
    return "\n".join(lines)


def _handover_prompt(lang: str, facts: str, extra: str = "") -> list[dict]:
    language = "Turkish" if lang == "tr" else "English"
    system = (f"You write a handover report from a student club's outgoing board to the incoming board, in {language}. Use ONLY the "
              f"recorded data. Plain text with these short sections, headings in {language}: {HANDOVER_SECTIONS[lang]}. "
              f"Never invent names, numbers, dates or outcomes; do not compute new figures or percentages; a field marked '-' is "
              f"simply not mentioned. In the last section give 3 to 5 concrete suggestions, each tied to a recorded fact. "
              f"Do not rank or judge individual people. No emojis.")
    return [{"role": "system", "content": system},
            {"role": "user", "content": f"RECORDED DATA:\n{facts}\n\nWrite the report.{extra}"}]


async def handover(chat_id: int, today: date) -> dict:
    facts = handover_facts(chat_id)
    lang = detect_lang(db.get_messages(chat_id)[:200])

    def problems(text):
        return report.unsupported_figures(text, facts) + meetings.unsupported_names(text, facts)

    text = (await llm.chat(_handover_prompt(lang, facts), temperature=0.2)).strip()
    bad = problems(text)
    if bad:
        extra = f"\nYour previous draft contained figures or names that are not in the data: {', '.join(bad)}. Remove them."
        text = (await llm.chat(_handover_prompt(lang, facts, extra), temperature=0.0)).strip()
        bad = problems(text)
        if bad:
            raise report.ReportRejected(bad)
    out = {"text": text, "model": llm.MODEL, "date": today.isoformat()}
    out["saved_id"] = db.save_ai(chat_id, "handover", f"{today:%Y-%m-%d}", out, llm.MODEL)
    return out


# ---- overlooked: deterministic checks over the records (no model) ------------------------------------------

OVERLOAD = 3


def overlooked(chat_id: int, today: date) -> dict[str, list[dict]]:
    """Things that slip through, found by plain rules over the records. Each entry: {id, title, note}."""
    items = db.get_items(chat_id)
    t, soon = today.isoformat(), (today + timedelta(days=HORIZON)).isoformat()
    open_tasks = [i for i in items if i["kind"] == "task" and i["status"] != "done"]
    out: dict[str, list[dict]] = {"undated": [], "events_bare": [], "no_feedback": [], "overloaded": [], "meetings_empty": [],
                                  "pending_ai": []}
    for x in open_tasks:
        if not x["due"]:
            out["undated"].append({"id": x["id"], "title": x["title"], "note": x["owner"] or ""})
    for e in items:
        if e["kind"] != "event":
            continue
        linked = [x for x in open_tasks if x["event_id"] == e["id"]]
        has_any = any(x["event_id"] == e["id"] for x in items if x["kind"] == "task")
        if e["phase"] in ("idea", "planning", "confirmed") and e["due"] and t <= e["due"] <= soon:
            if not has_any:
                out["events_bare"].append({"id": e["id"], "title": e["title"], "note": f"{e['due']} · bağlı görev yok"})
            elif any(not x["owner"] for x in linked):
                n = sum(1 for x in linked if not x["owner"])
                out["events_bare"].append({"id": e["id"], "title": e["title"], "note": f"{e['due']} · {n} görevin sorumlusu yok"})
        if e["phase"] == "held" and e.get("feedback_score") is None and not (e.get("feedback_note") or e.get("feedback_good")
                                                                              or e.get("feedback_bad") or e.get("feedback_comments")):
            out["no_feedback"].append({"id": e["id"], "title": e["title"], "note": e["due"] or ""})
    load: dict[str, int] = {}
    for x in open_tasks:
        if x["owner"]:
            load[x["owner"]] = load.get(x["owner"], 0) + 1
    out["overloaded"] = [{"id": None, "title": n, "note": f"{c}"} for n, c in sorted(load.items(), key=lambda r: -r[1]) if c >= OVERLOAD]
    for m in db.get_meetings(chat_id):
        if m["status"] == "held" and not any(i["meeting_id"] == m["id"] for i in items):
            out["meetings_empty"].append({"id": m["id"], "title": m["title"], "note": m["date"] or ""})
    pend = len(db.get_items(chat_id, review="proposed"))
    if pend:
        out["pending_ai"].append({"id": None, "title": str(pend), "note": ""})
    return out


# ---- printable weekly report (open in the browser, "save as PDF") ------------------------------------

def weekly_html(chat_id: int, today: date) -> str:
    from html import escape as e
    chat, items = db.get_chat(chat_id), db.get_items(chat_id)
    tasks = [i for i in items if i["kind"] == "task"]
    open_ = [x for x in tasks if x["status"] != "done"]
    t = today.isoformat()
    saved = db.list_ai(chat_id, "week")
    week = saved[0]["body"] if saved else None

    def rows(xs, cols):
        return "".join("<tr>" + "".join(f"<td>{e(str(c(x) or '-'))}</td>" for c in cols) + "</tr>" for x in xs)

    overdue = [x for x in open_ if x["due"] and x["due"] < t]
    orphans = [x for x in open_ if not x["owner"]]
    events = sorted((x for x in items if x["kind"] == "event" and x["phase"] in ("idea", "planning", "confirmed")
                     and x["due"] and x["due"] >= t), key=lambda x: x["due"])[:5]
    meets = [m for m in db.get_meetings(chat_id) if m["status"] == "planned"][:4]
    steps = "".join(f"<tr><td>{i}</td><td><b>{e(s['action'])}</b><br><small>{e(s['why'])}</small></td>"
                    f"<td>{e(s['owner'] or '-')}</td><td>{e(s['unit'] or '-')}</td><td>{e(s['when'] or '-')}</td></tr>"
                    for i, s in enumerate(week["steps"], 1)) if week else ""
    ai = (f"<h2>Yapay zekâ değerlendirmesi</h2><p>{e(week['assessment'])}</p>" if week and week.get("assessment") else "")
    agenda = ("<h2>Toplantı gündemi önerisi</h2><ol>" + "".join(f"<li>{e(a)}</li>" for a in week["agenda"]) + "</ol>"
              if week and week.get("agenda") else "")
    plan = (f"<h2>Bu hafta sırayla yapılacaklar</h2><table><tr><th>#</th><th>Adım</th><th>Sorumlu</th><th>Komite</th><th>Tarih</th></tr>{steps}</table>"
            if steps else "<p><i>Henüz haftalık yol haritası üretilmedi: Kulüp durumu → Gemma asistanı.</i></p>")
    foot = (f"Gemma ({e(week['model'])}) tarafından, yalnızca kulübün kayıtlarından yazıldı · yol haritası tarihi {e(week['date'])}"
            if week else "")
    ov = overlooked(chat_id, today)
    lab = {"undated": "Tarihi girilmemiş açık görevler", "events_bare": "Yaklaşan etkinlik: görev veya sorumlu eksik",
           "no_feedback": "Gerçekleşti ama geri bildirim girilmemiş", "overloaded": "3 veya daha çok açık işi olanlar (sayı)",
           "meetings_empty": "Yapıldı ama kayıt çıkarılmamış toplantılar", "pending_ai": "Onay bekleyen yapay zekâ önerisi sayısı"}
    miss = "".join(f"<h3>{e(lab[k])}</h3><ul>" + "".join(f"<li>{e(v['title'])}" + (f" <small>({e(v['note'])})</small>" if v["note"] else "") + "</li>"
                                                         for v in vs[:6]) + "</ul>" for k, vs in ov.items() if vs)
    miss = f"<h2>Gözden kaçanlar</h2>{miss}" if miss else ""
    return f"""<!doctype html><html lang="tr"><head><meta charset="utf-8"><title>{e(chat['name'])} · Haftalık rapor</title><style>
body{{font:14px/1.5 system-ui,Segoe UI,Arial,sans-serif;color:#111;max-width:820px;margin:24px auto;padding:0 20px}}
h1{{font-size:24px;margin:0}} h2{{font-size:16px;margin:22px 0 6px;border-bottom:2px solid #4f46e5;padding-bottom:3px;color:#312e81}}
.kpi{{display:flex;gap:10px;margin:14px 0}} .kpi div{{flex:1;border:1px solid #ddd;border-radius:8px;padding:8px;text-align:center}}
.kpi b{{display:block;font-size:22px}} table{{width:100%;border-collapse:collapse}} td,th{{border-bottom:1px solid #e5e7eb;padding:5px 6px;text-align:left;vertical-align:top}}
small{{color:#555}} footer{{margin-top:26px;font-size:12px;color:#666}} .bar{{margin-bottom:12px}} @media print{{.bar{{display:none}}body{{margin:0}}}}
</style></head><body><div class="bar"><button onclick="print()">PDF olarak kaydet / yazdır</button></div>
<h1>{e(chat['name'])}</h1><div style="color:#555">Haftalık yönetim raporu · {t}</div>
<div class="kpi"><div><b>{len(open_)}</b>açık görev</div><div><b>{len(tasks) - len(open_)}</b>biten görev</div>
<div><b>{len(overdue)}</b>geciken</div><div><b>{len(orphans)}</b>sorumlusuz</div></div>
{ai}{plan}{agenda}{miss}
<h2>Geciken işler</h2>{('<table>' + rows(overdue[:8], (lambda x: x['title'], lambda x: x['owner'], lambda x: x['due'])) + '</table>') if overdue else '<p>Yok.</p>'}
<h2>Sorumlusuz işler</h2>{('<table>' + rows(orphans[:8], (lambda x: x['title'], lambda x: x['unit'], lambda x: x['due'])) + '</table>') if orphans else '<p>Yok.</p>'}
<h2>Yaklaşan etkinlikler ve planlı toplantılar</h2>
{('<table>' + rows(events, (lambda x: x['title'], lambda x: x['due'], lambda x: x['place'])) + rows(meets, (lambda x: 'Toplantı: ' + x['title'], lambda x: x['date'], lambda x: ', '.join(x['units']))) + '</table>') if events or meets else '<p>Yok.</p>'}
<footer>{foot}</footer></body></html>"""
