import importlib

import pytest
from fastapi.testclient import TestClient

CHAT = "17.10.2026 19:33 - Ayşe: merhaba\n17.10.2026 19:34 - Mert: tamam\n"


@pytest.fixture()
def env(tmp_path, monkeypatch):
    monkeypatch.setenv("PANO_DB", str(tmp_path / "q.db"))
    from app import db
    db._conn = None
    importlib.reload(db)
    from app import main
    importlib.reload(main)
    c = TestClient(main.app)
    cid = c.post("/api/chats?units=Etkinlik,Medya", content=CHAT.encode()).json()["id"]
    return c, cid


def task(c, cid, title, owner, **kw):
    return c.post(f"/api/chats/{cid}/items", json={"title": title, "owner": owner, **kw}).json()["id"]


def test_people_come_from_task_owners_with_counts_only(env):
    c, cid = env
    task(c, cid, "Afiş", "Ayşe Yılmaz", due="2020-01-01", unit="Medya")
    done = task(c, cid, "Anket", "ayşe  yılmaz")      # same person, other spelling
    c.patch(f"/api/items/{done}", json={"status": "done"})
    task(c, cid, "Sponsor", "Mert Demir", due="2099-01-01")
    task(c, cid, "Sahipsiz", None)
    c.post(f"/api/chats/{cid}/items", json={"kind": "question", "title": "Soru?", "owner": "Ali"})
    ppl = {p["name"]: p for p in c.get(f"/api/chats/{cid}/people").json()["people"]}
    assert set(ppl) == {"Ayşe Yılmaz", "Mert Demir"}
    assert (ppl["Ayşe Yılmaz"]["open"], ppl["Ayşe Yılmaz"]["late"], ppl["Ayşe Yılmaz"]["done"]) == (1, 1, 1)
    assert ppl["Ayşe Yılmaz"]["committees"] == ["Medya"] and ppl["Mert Demir"]["late"] == 0
    assert not any("score" in k or "rank" in k for k in ppl["Mert Demir"])


def test_person_detail_events_meetings_and_committees(env):
    c, cid = env
    ev = c.post(f"/api/chats/{cid}/items", json={"kind": "event", "title": "Söyleşi", "owner": "Mert Demir"}).json()["id"]
    task(c, cid, "Afiş", "Ayşe Yılmaz", due="2099-05-01", event_id=ev)
    task(c, cid, "Bilet", "Ayşe Yılmaz", due="2099-02-01")
    c.patch(f"/api/chats/{cid}", json={"unit_members": {"Etkinlik": "Ayşe Yılmaz, Can"}})
    c.post(f"/api/chats/{cid}/meetings", json={"title": "Haftalık", "attendees": "Can, ayşe yılmaz"})
    c.post(f"/api/chats/{cid}/meetings", json={"title": "Başka", "attendees": "Mert Demir"})
    d = c.get(f"/api/chats/{cid}/person", params={"name": "Ayşe Yılmaz"}).json()
    assert [t["title"] for t in d["upcoming"]] == ["Bilet", "Afiş"] and d["late"] == []
    assert d["events"] == [{"id": ev, "title": "Söyleşi", "due": None, "phase": "idea", "role": ["task"]}]
    assert [m["title"] for m in d["meetings"]] == ["Haftalık"] and "Etkinlik" in d["committees"]
    assert c.get(f"/api/chats/{cid}/person", params={"name": "Yok Kişi"}).status_code == 404
