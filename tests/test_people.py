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


def test_workload_counts_per_person_and_committee_without_ranking(env):
    c, cid = env
    task(c, cid, "Afis", "Ayse Yilmaz", due="2020-01-01", unit="Medya")
    task(c, cid, "Anket", "ayse  yilmaz", due="2099-01-01", unit="Medya")
    done = task(c, cid, "Biten", "Ayse Yilmaz", due="2020-01-01", unit="Medya")
    c.patch(f"/api/items/{done}", json={"status": "done"})
    task(c, cid, "Sponsor", "Mert Demir", unit="Etkinlik")
    task(c, cid, "Sahipsiz gec", None, due="2020-02-02")
    c.post(f"/api/chats/{cid}/items", json={"kind": "question", "title": "Soru?", "owner": "Ali"})
    w = c.get(f"/api/chats/{cid}/workload").json()
    ppl = {p["name"]: (p["open"], p["late"]) for p in w["people"]}
    assert ppl == {"Ayse Yilmaz": (2, 1), "Mert Demir": (1, 0)}      # done and non-task records are not counted
    assert [p["name"] for p in w["people"]] == sorted(ppl)            # alphabetical, never ranked by load
    assert {u["unit"]: (u["open"], u["late"]) for u in w["units"]} == {"Etkinlik": (1, 0), "Medya": (2, 1)}
    assert w["no_owner"] == {"open": 1, "late": 1} and w["no_unit"] == {"open": 1, "late": 1}   # shown, not hidden
    assert not any(k in p for p in w["people"] + w["units"] for k in ("score", "rank", "done"))
    assert c.get("/api/chats/9999/workload").status_code == 404