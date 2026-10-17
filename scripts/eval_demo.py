"""Run the full pipeline on a demo chat and score it against hand-written expectations.

    python scripts/eval_demo.py            # Turkish demo
    python scripts/eval_demo.py en         # English demo
    PANO_MODEL=gemma4:e2b python scripts/eval_demo.py

Uses a throwaway database, so it never touches your real boards.
"""
from __future__ import annotations

import asyncio
import json
import os
import sys
import tempfile
import time
from collections import Counter
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
os.environ["PANO_DB"] = str(Path(tempfile.mkdtemp()) / "eval.db")

from app import analyzer, db, llm  # noqa: E402
from app.analyzer import norm  # noqa: E402
from app.main import DEMOS  # noqa: E402
from app.parser import parse_chat, read_export  # noqa: E402

# Each check: (description, kind, keywords that must all appear in one item, extra condition)
CHECKS = {
    "tr": [
        ("Söyleşi etkinliği 31 Ekim'de (24'ten taşındı)", "event", ["soylesi"], lambda i: i["due"] == "2026-10-31"),
        ("Hazırlık toplantısı 23 Ekim", "event", ["toplanti"], lambda i: i["due"] == "2026-10-23"),
        ("Salon dilekçesi → Deniz, bitti", "task", ["dilekce"], lambda i: (i["owner"] or "").startswith("Deniz") and i["status"] == "done"),
        ("Afiş → Zeynep", "task", ["afis"], lambda i: (i["owner"] or "").startswith("Zeynep")),
        ("Kayıt formu → Can, bitti", "task", ["form"], lambda i: (i["owner"] or "").startswith("Can") and i["status"] == "done"),
        ("Sertifika → Selin (Can'dan devraldı)", "task", ["sertifika"], lambda i: (i["owner"] or "").startswith("Selin")),
        ("Story serisi → Ece", "task", ["story"], lambda i: (i["owner"] or "").startswith("Ece")),
        ("Projeksiyon/ses dilekçesi: sahibi yok", "task", ["teknik"], lambda i: not i["owner"] and i["status"] == "open"),
        ("Cevapsız: sponsor dosyası", "question", ["sponsor", "dosya"], lambda i: i["status"] == "open"),
        ("Cevapsız: yaka mikrofonu", "question", ["mikrofon"], lambda i: i["status"] == "open"),
        ("Cevapsız: kahveci teslimat saati", "question", ["teslimat"], lambda i: i["status"] == "open"),
        ("Karar: söyleşi 31 Ekim", "decision", ["31"], None),
        ("Karar: Google Forms", "decision", ["form"], None),
        ("Karar: tişört lacivert", "decision", ["lacivert"], None),
    ],
    "en": [
        ("Fair booth moved to Oct 30", "event", ["fair"], lambda i: i["due"] == "2026-10-30"),
        ("Prep call Oct 22", "event", ["call"], lambda i: i["due"] == "2026-10-22"),
        ("Line follower fix → Noah, done", "task", ["line"], lambda i: (i["owner"] or "").startswith("Noah") and i["status"] == "done"),
        ("Banner → Priya", "task", ["banner"], lambda i: (i["owner"] or "").startswith("Priya")),
        ("Lab booking → Leo, done", "task", ["lab"], lambda i: (i["owner"] or "").startswith("Leo") and i["status"] == "done"),
        ("Sign-up form → Noah, done", "task", ["form"], lambda i: (i["owner"] or "").startswith("Noah") and i["status"] == "done"),
        ("Stickers → Ava, due Oct 28", "task", ["sticker"], lambda i: (i["owner"] or "").startswith("Ava") and i["due"] == "2026-10-28"),
        ("Print shop: nobody owns it", "task", ["print"], lambda i: not i["owner"] and i["status"] == "open"),
        ("Unanswered: cabinet key", "question", ["key"], lambda i: i["status"] == "open"),
        ("Unanswered: extension cords", "question", ["extension"], lambda i: i["status"] == "open"),
        ("Unanswered: snack delivery time", "question", ["deliver"], lambda i: i["status"] == "open"),
        ("Decision: booth on Oct 30, show both robots", "decision", ["30"], None),
        ("Decision: Google Forms", "decision", ["form"], None),
    ],
}


def check(items, kind, words, cond):
    for i in items:
        if i["kind"] != kind:
            continue
        text = norm(" ".join(filter(None, [i["title"], i["place"]])))
        if all(w in text for w in words) and (cond is None or cond(i)):
            return i
    return None


async def main(lang: str) -> None:
    health = await llm.health()
    if not health["model_ready"]:
        sys.exit(f"Model not ready: {health}")
    name, path, units = DEMOS[lang]
    chat_id = db.create_chat(name, units, parse_chat(read_export(path.read_bytes())))
    t0 = time.time()
    await analyzer.analyze(chat_id)
    took = time.time() - t0
    p = analyzer.progress(chat_id)
    if p["state"] == "error":
        sys.exit(f"Analysis failed: {p['error']}")

    items = db.get_items(chat_id, review=None)  # every proposal, whatever its review state
    print(f"\n=== {name} · {llm.MODEL} · {p['total']} windows · {took:.0f}s ===\n")
    for kind in ("task", "question", "decision", "event"):
        print(kind.upper())
        for i in (x for x in items if x["kind"] == kind):
            extra = " | ".join(filter(None, [i["owner"], i["due"], i["time"], i["unit"], i["place"]]))
            print(f"  [{i['status']:8}] {i['title']}  ({extra})  #{i['source_idx']}")
    print()
    passed = 0
    for desc, kind, words, cond in CHECKS[lang]:
        ok = check(items, kind, words, cond) is not None
        passed += ok
        print(f"  {'✅' if ok else '❌'} {desc}")
    print(f"\nScore: {passed}/{len(CHECKS[lang])}  ·  {len(items)} items  ·  {took:.0f}s")
    by_kind = Counter(i["kind"] for i in items)
    no_src = sum(1 for i in items if i["needs_review"] == 1)
    bad_date = sum(1 for i in items if i["needs_review"] == 2)
    print(f"Proposals by kind: {dict(by_kind)} · no source (1): {no_src} · date unclear (2): {bad_date}\n")
    # Demo data only (fake chats), so the raw list is safe to keep; data/ is git-ignored anyway.
    out = ROOT / "data" / "eval_runs"
    out.mkdir(parents=True, exist_ok=True)
    f = out / f"{lang}-{datetime.now():%Y%m%d-%H%M%S}.json"
    f.write_text(json.dumps({
        "chat": name, "model": llm.MODEL, "seconds": round(took), "score": f"{passed}/{len(CHECKS[lang])}",
        "by_kind": by_kind, "needs_review_1": no_src, "needs_review_2": bad_date, "items": items,
    }, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Saved: {f}")
    print(f"DB: {os.environ['PANO_DB']}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    asyncio.run(main(sys.argv[1] if len(sys.argv) > 1 else "tr"))
