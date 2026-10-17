import importlib

import pytest
from fastapi.testclient import TestClient

CHAT = "17.10.2026 19:33 - Ayşe: Afişi ben yaparım\n17.10.2026 19:34 - Mert: tamam\n"


@pytest.fixture()
def env(tmp_path, monkeypatch):
    monkeypatch.setenv("PANO_DB", str(tmp_path / "ev.db"))
    from app import db
    db._conn = None
    importlib.reload(db)
    from app import main
    importlib.reload(main)
    c = TestClient(main.app)
    cid = c.post("/api/chats?units=Etkinlik,Teknik", content=CHAT.encode()).json()["id"]
    return c, cid


def board(c, cid):
    return c.get(f"/api/chats/{cid}/board").json()


FULL = {"kind": "event", "title": "Söyleşi", "due": "2026-10-31", "time": "14:00", "place": "Amfi 2",
        "owner": "Ayşe", "event_type": "söyleşi", "phase": "planning", "event_units": ["Etkinlik", "Teknik"],
        "attendees_expected": 120, "budget_est": 3500.5, "notes": "Konuk: Ahmet Bey"}


def test_create_event_with_all_fields_and_phase_default(env):
    c, cid = env
    ev = c.post(f"/api/chats/{cid}/items", json=FULL).json()
    for k, v in FULL.items():
        assert ev[k] == v, k
    assert ev["review"] == "approved" and ev["attendees_actual"] is None and ev["budget_actual"] is None
    assert [e["title"] for e in board(c, cid)["events"]] == ["Söyleşi"]  # straight on the board

    bare = c.post(f"/api/chats/{cid}/items", json={"kind": "event", "title": "Fikir"}).json()
    assert bare["phase"] == "idea" and bare["event_units"] == []


def test_edit_clear_and_zero_values(env):
    c, cid = env
    ev = c.post(f"/api/chats/{cid}/items", json=FULL).json()
    r = c.patch(f"/api/items/{ev['id']}", json={"phase": "held", "attendees_actual": 0, "budget_actual": 0,
                                                "place": "", "event_units": ["Teknik"]}).json()
    assert r["phase"] == "held" and r["attendees_actual"] == 0 and r["budget_actual"] == 0  # 0 is a value
    assert r["place"] is None and r["event_units"] == ["Teknik"] and r["time"] == "14:00"
    assert r["user_edited"] == 1


def test_validation(env):
    c, cid = env
    ev = c.post(f"/api/chats/{cid}/items", json=FULL).json()
    url = f"/api/items/{ev['id']}"
    assert c.patch(url, json={"phase": "bitti"}).status_code == 400
    assert c.patch(url, json={"budget_est": -1}).status_code == 400
    assert c.patch(url, json={"attendees_expected": -5}).status_code == 400
    assert c.patch(url, json={"event_id": ev["id"]}).status_code == 400
    task = c.post(f"/api/chats/{cid}/items", json={"title": "iş"}).json()
    assert c.patch(f"/api/items/{task['id']}", json={"phase": "idea"}).status_code == 400
    assert c.post(f"/api/chats/{cid}/items", json={"title": "x", "budget_est": 5}).status_code == 400
    assert c.post(f"/api/chats/{cid}/items", json={"title": "x", "event_id": 9999}).status_code == 400
    assert c.get(f"/api/chats/{cid}/board").json()["events"][0]["phase"] == "planning"


def test_link_tasks_and_decisions_to_event(env):
    c, cid = env
    ev = c.post(f"/api/chats/{cid}/items", json=FULL).json()
    task = c.post(f"/api/chats/{cid}/items", json={"title": "Afiş", "event_id": ev["id"]}).json()
    dec = c.post(f"/api/chats/{cid}/items", json={"kind": "decision", "title": "31 Ekim"}).json()
    assert c.patch(f"/api/items/{dec['id']}", json={"event_id": ev["id"]}).json()["event_id"] == ev["id"]
    b = board(c, cid)
    assert [t["event_id"] for t in b["tasks"]] == [ev["id"]] and b["decisions"][0]["event_id"] == ev["id"]

    # another chat's event cannot be linked
    other = c.post("/api/chats", content=CHAT.encode() + b"17.10.2026 19:40 - Ali: selam\n").json()["id"]
    foreign = c.post(f"/api/chats/{other}/items", json={"kind": "event", "title": "Başka"}).json()
    assert c.patch(f"/api/items/{task['id']}", json={"event_id": foreign["id"]}).status_code == 400

    # deleting the event keeps the task, just unlinks it
    c.delete(f"/api/items/{ev['id']}")
    assert board(c, cid)["tasks"][0]["event_id"] is None


def test_cancelled_event_is_not_the_next_event(env):
    c, cid = env
    ev = c.post(f"/api/chats/{cid}/items", json={**FULL, "due": "2099-01-01"}).json()
    assert board(c, cid)["overview"]["kpi"]["next_event"] is not None
    c.patch(f"/api/items/{ev['id']}", json={"phase": "cancelled"})
    assert board(c, cid)["overview"]["kpi"]["next_event"] is None
