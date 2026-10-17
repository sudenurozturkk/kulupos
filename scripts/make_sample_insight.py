"""Write the precomputed period insight of the sample club into demo/seed-insight-tr.json (needs Ollama running).

    python scripts/make_sample_insight.py

Uses a throwaway database. The text is whatever the local model produced and passed the figure check;
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

from app import analysis, db, llm, seed  # noqa: E402

PATH = ROOT / "demo" / "seed-insight-tr.json"


async def main() -> None:
    health = await llm.health()
    if not health["model_ready"]:
        sys.exit(f"Model not ready: {health}")
    PATH.unlink(missing_ok=True)
    chat_id = seed.seed_sample(date.today())
    r = await analysis.generate(analysis.compute(db.get_items(chat_id)), "tr")
    PATH.write_text(json.dumps({"lang": "tr", "model": r["model"], "insight": r["insight"]},
                               ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(r["insight"])


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    asyncio.run(main())
