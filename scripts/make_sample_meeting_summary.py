"""Write the precomputed summary of the sample club's held meeting into demo/seed-meeting-summary-tr.json
(needs Ollama running).

    python scripts/make_sample_meeting_summary.py

Uses a throwaway database. The text is whatever the local model produced and passed the figure and name check;
nothing is edited by hand.
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

from app import db, llm, meetings, seed  # noqa: E402

PATH = ROOT / "demo" / "seed-meeting-summary-tr.json"
KEY = "yonetim"


async def main() -> None:
    health = await llm.health()
    if not health["model_ready"]:
        sys.exit(f"Model not ready: {health}")
    PATH.unlink(missing_ok=True)
    chat_id = seed.seed_sample(date.today())
    title = next(m["title"] for m in json.loads(seed.MEETINGS.read_text(encoding="utf-8"))["meetings"] if m["key"] == KEY)
    meeting = next(m for m in db.get_meetings(chat_id) if m["title"] == title)
    r = await meetings.summarize(meeting)
    PATH.write_text(json.dumps({"key": KEY, "lang": r["lang"], "model": r["model"], "summary": r["body"]},
                               ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(r["body"])


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    asyncio.run(main())
