"""G18 event analysis: computed figures, new event fields, migration, insight figure check, sample insight."""
import importlib
import sqlite3
from datetime import date

from fastapi.testclient import TestClient

CHAT = "17.10.2026 19:33 - Ayşe: merhaba\n17.10.2026 19:34 - Mert: selam\n"


def setup(tmp_path, monkeypatch, name="a.db"):
    monkeypatch.setenv("PANO_DB", str(tmp_path / name))
    from app import db
    db._conn = None
    importlib.reload(db)
    from app import analysis, main, seed
    importlib.reload(analysis)
    importlib.reload(seed)
    importlib.reload(main)
    return db, analysis, main


def make_events(db, cid):
    db.add_item(cid, "event", title="A", due="2026-03-01", phase="held", event_units=["Etkinlik", "Sosyal"],
                attendees_expected=100, attendees_actual=80, applications=160, budget_est=1000, budget_actual=1250,
                feedback_score=4, feedback_note="iyi")
    db.add_item(cid, "event", title="B", due="2026-04-01", phase="held", event_units=["Etkinlik"],
                attendees_expected=50, attendees_actual=20)
    db.add_item(cid, "event", title="C", due="2026-05-01", phase="planning")
    db.add_item(cid, "event", title="D", due="2026-06-01", phase="cancelled", attendees_expected=10)
    db.add_item(cid, "event", title="E", phase="held", attendees_actual=5, review="proposed")  # not approved


def test_compute_numbers_and_gaps(tmp_path, monkeypatch):
    db, analysis, main = setup(tmp_path, monkeypatch)
    with TestClient(main.app) as c:
        cid = c.post("/api/chats", content=CHAT.encode()).json()["id"]
        make_events(db, cid)
        a = c.get(f"/api/chats/{cid}/event-analysis").json()
    assert a["total"] == 3 and [r["title"] for r in a["events"]] == ["A", "B", "C"]  # cancelled/proposed out
    ra, rb, rc = a["events"]
    assert (ra["attendance_pct"], ra["conversion_pct"], ra["budget_dev"], ra["budget_dev_pct"]) == (80, 50, 250, 25)
    assert rb["attendance_pct"] == 40 and rb["conversion_pct"] is None and rb["budget_dev"] is None
    assert rc["attendance_pct"] is None and rc["actual"] is None and rc["feedback_score"] is None
    assert a["avg_attendees"] == 50 and a["avg_attendance_pct"] == 60 and a["avg_feedback"] == 4
    assert a["highest"] == {"title": "A", "actual": 80} and a["lowest"] == {"title": "B", "actual": 20}
    assert {x["unit"]: x["events"] for x in a["committees"]} == {"Etkinlik": 2, "Sosyal": 1, None: 1}
    assert a["insight"] is None


def test_single_event_has_no_lowest_and_zero_division_is_safe(tmp_path, monkeypatch):
    db, analysis, main = setup(tmp_path, monkeypatch)
    items = [{"kind": "event", "id": 1, "title": "Z", "phase": "held", "due": None, "event_units": [],
              "attendees_expected": 0, "attendees_actual": 5, "applications": 0, "budget_est": 0, "budget_actual": 10,
              "feedback_score": None, "feedback_note": None}]
    s = analysis.compute(items)
    r = s["events"][0]
    assert r["attendance_pct"] is None and r["conversion_pct"] is None and r["budget_dev"] == 10
    assert r["budget_dev_pct"] is None and s["lowest"] is None and s["highest"]["actual"] == 5
    assert analysis.compute([])["total"] == 0 and analysis.compute([])["avg_attendees"] is None


def test_event_fields_validation(tmp_path, monkeypatch):
    db, analysis, main = setup(tmp_path, monkeypatch)
    with TestClient(main.app) as c:
        cid = c.post("/api/chats", content=CHAT.encode()).json()["id"]
        ev = c.post(f"/api/chats/{cid}/items", json={"kind": "event", "title": "X", "applications": 30,
                                                      "feedback_score": 4.5, "feedback_note": " güzel "}).json()
        assert (ev["applications"], ev["feedback_score"], ev["feedback_note"]) == (30, 4.5, "güzel")
        for bad in ({"feedback_score": 6}, {"feedback_score": 0.5}, {"applications": -1}):
            assert c.patch(f"/api/items/{ev['id']}", json=bad).status_code == 400
        assert c.patch(f"/api/items/{ev['id']}", json={"feedback_score": None, "feedback_note": ""}).json()["feedback_score"] is None
        task = c.post(f"/api/chats/{cid}/items", json={"kind": "task", "title": "t"}).json()
        assert c.patch(f"/api/items/{task['id']}", json={"applications": 3}).status_code == 400


def test_old_database_is_migrated(tmp_path, monkeypatch):
    path = tmp_path / "old.db"
    con = sqlite3.connect(path)  # items table as it was before G18: no applications/feedback columns
    con.executescript("""CREATE TABLE chats (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL,
        units TEXT NOT NULL DEFAULT '[]', imported_at TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'imported',
        error TEXT, analyzed_upto INTEGER NOT NULL DEFAULT -1);
        CREATE TABLE items (id INTEGER PRIMARY KEY AUTOINCREMENT, chat_id INTEGER NOT NULL, kind TEXT NOT NULL,
        title TEXT NOT NULL, owner TEXT, due TEXT, time TEXT, place TEXT, unit TEXT, status TEXT NOT NULL DEFAULT 'open',
        source_idx INTEGER, resolved_idx INTEGER, user_edited INTEGER NOT NULL DEFAULT 0,
        created_at TEXT NOT NULL, updated_at TEXT NOT NULL);
        INSERT INTO chats (name, imported_at) VALUES ('eski', '2026-01-01');
        INSERT INTO items (chat_id, kind, title, created_at, updated_at) VALUES (1, 'event', 'Eski', 'x', 'x');""")
    con.commit()
    con.close()
    db, analysis, main = setup(tmp_path, monkeypatch, "old.db")
    ev = db.get_item(1)
    assert ev["applications"] is None and ev["feedback_score"] is None and ev["feedback_note"] is None
    db.update_item(1, applications=7)
    assert db.get_item(1)["applications"] == 7


def test_insight_accepts_computed_figures_and_rejects_invented_ones(tmp_path, monkeypatch):
    db, analysis, main = setup(tmp_path, monkeypatch)
    calls = []

    async def fake(messages, **k):
        calls.append(messages)
        return replies.pop(0)
    monkeypatch.setattr(analysis.llm, "chat", fake)
    with TestClient(main.app) as c:
        cid = c.post("/api/chats", content=CHAT.encode()).json()["id"]
        assert c.post(f"/api/chats/{cid}/event-analysis/insight").status_code == 400  # no events
        make_events(db, cid)

        replies = ["Ortalama katılım 50 kişi, A en yüksek (80)."]
        r = c.post(f"/api/chats/{cid}/event-analysis/insight")
        assert r.status_code == 200 and r.json()["insight"].startswith("Ortalama") and r.json()["stale"] is False
        assert len(calls) == 1 and "[held]" in calls[0][1]["content"] and "Girilmedi" in calls[0][1]["content"]

        replies = ["Katılım %99 oldu.", "Katılım yine 99 kişi."]  # invented figure twice -> rejected, old text kept
        r = c.post(f"/api/chats/{cid}/event-analysis/insight")
        assert r.status_code == 422 and r.json()["detail"]["unsupported"] == ["99"]
        assert c.get(f"/api/chats/{cid}/event-analysis").json()["insight"].startswith("Ortalama")

        replies = ["Katılım 77 kişi.", "Ortalama katılım 50 kişi."]  # first draft invents a figure, retry is clean
        assert c.post(f"/api/chats/{cid}/event-analysis/insight").status_code == 200

        db.update_item(db.get_items(cid, "event")[0]["id"], attendees_actual=81)
        assert c.get(f"/api/chats/{cid}/event-analysis").json()["stale"] is True


def test_sample_club_has_filled_held_event_and_fresh_precomputed_insight(tmp_path, monkeypatch):
    db, analysis, main = setup(tmp_path, monkeypatch)
    from app import report, seed
    cid = seed.seed_sample(date(2026, 10, 17))
    stats = analysis.compute(db.get_items(cid))
    held = [r for r in stats["events"] if r["phase"] == "held"]
    assert len(held) == 1 and "örnek veri" in held[0]["title"].lower()
    assert None not in (held[0]["attendance_pct"], held[0]["conversion_pct"], held[0]["budget_dev"], held[0]["feedback_score"])
    row = db.get_insight(cid)
    view = analysis.insight_view(stats, row)
    assert view["source"] == "sample" and view["stale"] is False
    assert report.unsupported_figures(row["body"], analysis.facts_text(stats, row["lang"])) == []
