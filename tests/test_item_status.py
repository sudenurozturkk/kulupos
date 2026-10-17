import importlib

import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def env(tmp_path, monkeypatch):
    monkeypatch.setenv("PANO_DB", str(tmp_path / "t.db"))
    from app import db
    importlib.reload(db)
    from app import analyzer, main
    importlib.reload(analyzer)
    importlib.reload(main)
    client = TestClient(main.app)
    chat = client.post("/api/chats", content=b"17.10.2026 19:33 - Ay\xc5\x9fe: Merhaba\n").json()
    return db, client, chat["id"]


def add(client, chat_id, kind, title):
    return client.post(f"/api/chats/{chat_id}/items", json={"kind": kind, "title": title}).json()["id"]


def test_question_resolved_and_invalid_leave_open_lists_and_log_history(env):
    db, client, cid = env
    q1, q2 = add(client, cid, "question", "Salon kim?"), add(client, cid, "question", "Eski soru")
    r = client.patch(f"/api/items/{q1}", json={"status": "resolved", "note": "Salon B-201 oldu"})
    assert r.status_code == 200 and r.json()["status"] == "resolved"
    client.patch(f"/api/items/{q2}", json={"status": "invalid"})
    b = client.get(f"/api/chats/{cid}/board").json()
    assert b["missed"]["questions"] == []
    assert {q["status"] for q in b["questions"]} == {"resolved", "invalid"}
    h = client.get(f"/api/items/{q1}/history").json()
    assert [(x["field"], x["old"], x["new"], x["note"]) for x in h] == [("status", "open", "resolved", "Salon B-201 oldu")]
    client.patch(f"/api/items/{q1}", json={"status": "open"})   # reopening is logged too
    assert [x["new"] for x in client.get(f"/api/items/{q1}/history").json()] == ["resolved", "open"]


def test_same_status_writes_no_history_and_other_kinds_reject_new_statuses(env):
    db, client, cid = env
    q, t = add(client, cid, "question", "Soru"), add(client, cid, "task", "Görev")
    client.patch(f"/api/items/{q}", json={"status": "open"})
    assert client.get(f"/api/items/{q}/history").json() == []
    assert client.patch(f"/api/items/{t}", json={"status": "resolved"}).status_code == 400
    assert client.patch(f"/api/items/{q}", json={"status": "bogus"}).status_code == 400
    assert client.get("/api/items/9999/history").status_code == 404


def test_user_closed_question_is_not_reopened_by_the_model(env, monkeypatch):
    db, client, cid = env
    q = add(client, cid, "question", "Salon kim?")
    client.patch(f"/api/items/{q}", json={"status": "invalid"})
    assert db.get_item(q)["user_edited"] == 1 and db.get_item(q)["status"] == "invalid"


def test_decision_validity_is_history_not_current(env):
    db, client, cid = env
    d1, d2, d3 = (add(client, cid, "decision", x) for x in ("Salon B-201", "Saat 14:00", "Lacivert afiş"))
    assert client.get(f"/api/chats/{cid}/board").json()["decisions"][0]["validity"] == "valid"
    assert client.patch(f"/api/items/{d1}", json={"validity": "changed", "note": "Salon A-100 oldu"}).status_code == 200
    client.patch(f"/api/items/{d2}", json={"validity": "cancelled"})
    client.patch(f"/api/items/{d3}", json={"title": "Lacivert ve beyaz afiş"})
    h1 = client.get(f"/api/items/{d1}/history").json()
    assert [(x["field"], x["old"], x["new"], x["note"]) for x in h1] == [("validity", "valid", "changed", "Salon A-100 oldu")]
    h3 = client.get(f"/api/items/{d3}/history").json()
    assert [(x["field"], x["old"], x["new"]) for x in h3] == [("title", "Lacivert afiş", "Lacivert ve beyaz afiş")]
    # current counts and alerts leave out changed/cancelled decisions; the record itself stays visible
    b = client.get(f"/api/chats/{cid}/board").json()
    assert b["overview"]["kpi"]["decisions"] == 1 and len(b["overview"]["focus"]["decisions"]) == 1
    assert len(b["decisions"]) == 3
    rows = client.get(f"/api/chats/{cid}/export", params={"what": "decisions", "format": "json"}).json()["rows"]
    assert {r["title"]: r["validity"] for r in rows}["Salon B-201"] == "changed"


def test_validity_rules(env):
    db, client, cid = env
    t, d = add(client, cid, "task", "Görev"), add(client, cid, "decision", "Karar")
    assert client.patch(f"/api/items/{t}", json={"validity": "changed"}).status_code == 400
    assert client.patch(f"/api/items/{d}", json={"validity": "weird"}).status_code == 400
    client.patch(f"/api/items/{d}", json={"validity": "valid"})   # no change -> no history
    assert client.get(f"/api/items/{d}/history").json() == []


def test_changed_decision_is_not_a_fact_in_meeting_summary(env):
    db, client, cid = env
    from app import meetings
    mid = db.add_meeting(cid, title="T", date="2026-10-14", notes="Karar: x", status="held", units=[])
    d = db.add_item(cid, "decision", title="Salon B-201", meeting_id=mid)
    before = meetings.summary_fingerprint(db.get_meeting(mid), "tr")
    assert "Salon B-201" in meetings.facts_text(db.get_meeting(mid), "tr")
    client.patch(f"/api/items/{d}", json={"validity": "changed"})
    m = db.get_meeting(mid)
    assert "Salon B-201" not in meetings.facts_text(m, "tr")
    assert meetings.summary_fingerprint(m, "tr") != before   # saved summary turns stale
