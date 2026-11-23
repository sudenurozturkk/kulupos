"""The meetings month grid is plain JS; run its pure function with node (skipped when node is not installed)."""
import json
import re
import shutil
import subprocess
from pathlib import Path

import pytest

SRC = (Path(__file__).resolve().parent.parent / "static" / "app.js").read_text(encoding="utf-8")


def grid(year, month0, meetings):
    fn = re.search(r"function monthCells\(.*?\n}\n", SRC, re.S).group(0)
    js = fn + f"console.log(JSON.stringify(monthCells({year}, {month0}, {json.dumps(meetings)})));"
    out = subprocess.run(["node", "-e", js], capture_output=True, text=True, check=True, timeout=30).stdout
    return json.loads(out)


pytestmark = pytest.mark.skipif(shutil.which("node") is None, reason="node not installed")


def test_month_grid_shape_and_placement():
    ms = [{"id": 1, "title": "B", "date": "2026-11-23", "time": "18:00", "status": "planned"},
          {"id": 2, "title": "A", "date": "2026-11-23", "time": "09:30", "status": "held"},
          {"id": 3, "title": "NoTime", "date": "2026-11-23", "time": None, "status": "planned"},
          {"id": 4, "title": "Undated", "date": None, "time": None, "status": "planned"},
          {"id": 5, "title": "Other month", "date": "2026-12-01", "time": None, "status": "planned"}]
    weeks = grid(2026, 10, ms)                       # November 2026 starts on a Sunday -> Monday-first grid
    assert all(len(w) == 7 for w in weeks) and len(weeks) == 6
    flat = [c for w in weeks for c in w]
    assert flat[0]["iso"] == "2026-10-26" and not flat[0]["inMonth"]
    assert sum(c["inMonth"] for c in flat) == 30
    day = next(c for c in flat if c["iso"] == "2026-11-23")
    assert [m["id"] for m in day["meetings"]] == [2, 1, 3]       # by time; no time last
    assert [m["id"] for c in flat for m in c["meetings"]] == [2, 1, 3, 5]   # Dec 1 shows in the trailing cell; undated never
    assert next(c for c in flat if c["iso"] == "2026-12-01")["meetings"][0]["id"] == 5


def test_month_grid_leap_february_and_year_wrap():
    feb = grid(2028, 1, [])
    assert sum(c["inMonth"] for w in feb for c in w) == 29
    assert grid(2026, 11, [])[0][0]["iso"] == "2026-11-30"        # December 2026 starts on Tuesday
    assert grid(2027, 0, [])[0][0]["iso"] == "2026-12-28"         # January 2027 starts on Friday