"""Write what the local model produces for the sample club into demo/seed-ai-tr.json (needs Ollama running; ~5 min):
task/decision/question suggestions from the held meeting's notes, event ideas from the held events, and an event plan.

    python scripts/make_sample_ai.py

Uses a throwaway database. Nothing is edited by hand; the seed loads this file so the sample club ships with real
model output (source = sample).
"""
from __future__ import annotations

import asyncio
import json
import os
import sys
import tempfile
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
os.environ["PANO_DB"] = str(Path(tempfile.mkdtemp()) / "sample.db")

from app import coach, db, insights, llm, meetings, seed  # noqa: E402

PATH = ROOT / "demo" / "seed-ai-tr.json"
HELD_MEETING = "yonetim"
GOAL = "Kasım ayında 150 kişilik bir siber güvenlik çalıştayı düzenlemek istiyoruz"


async def main() -> None:
    health = await llm.health()
    if not health["model_ready"]:
        sys.exit(f"Model not ready: {health}")
    done = json.loads(PATH.read_text(encoding="utf-8")) if PATH.exists() else {}   # only missing parts are generated
    today = date.today()
    chat_id = seed.seed_sample(today)
    spec = json.loads(seed.MEETINGS.read_text(encoding="utf-8"))
    title = next(m["title"] for m in spec["meetings"] if m["key"] == HELD_MEETING)
    meeting = next(m for m in db.get_meetings(chat_id) if m["title"] == title)
    out = {"model": llm.MODEL, "meeting": HELD_MEETING, **done}
    if "proposals" not in done:
        for i in db.get_items(chat_id, review="proposed"):
            if i["meeting_id"] == meeting["id"]:
                db.delete_item(i["id"])
        db.update_meeting(meeting["id"], analyzed_fp=None)
        await meetings.analyze(meeting["id"])
        out["proposals"] = [{"kind": i["kind"], "title": i["title"], "unit": i["unit"], "owner": i["owner"], "due": i["due"],
                             "source_text": i["source_text"]}
                            for i in db.get_items(chat_id, review="proposed") if i["meeting_id"] == meeting["id"]]
    if "ideas" not in done:
        out["ideas"] = await insights.suggest_events(chat_id, today)
    if "plan" not in done:
        out["plan"] = {**await insights.plan_event(chat_id, GOAL, today), "goal": GOAL}
    if "week" not in done:
        out["week"] = await coach.week_plan(chat_id, today)
    if "handover" not in done:
        out["handover"] = await coach.handover(chat_id, today)
    PATH.write_text(json.dumps(out, ensure_ascii=False, indent=2) + chr(10), encoding="utf-8")
    print("parts:", sorted(k for k in out if k not in ("model", "meeting")))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    asyncio.run(main())
