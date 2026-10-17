import importlib

import pytest
from fastapi.testclient import TestClient

CHAT = "17.10.2026 19:33 - Ayşe: Afişi ben yaparım\n17.10.2026 19:34 - Mert: tamam\n"


@pytest.fixture()
def env(tmp_path, monkeypatch):
    monkeypatch.setenv("PANO_DB", str(tmp_path / "u.db"))
    from app import db
    db._conn = None
    importlib.reload(db)
    from app import main
    importlib.reload(main)
    c = TestClient(main.app)
    cid = c.post("/api/chats?units=Etkinlik,Sosyal,Teknik", content=CHAT.encode()).json()["id"]
    for unit in ("Etkinlik", "Sosyal", None):
        c.post(f"/api/chats/{cid}/items", json={"title": f"iş {unit}", "unit": unit})
    return c, cid


def board(c, cid):
    return c.get(f"/api/chats/{cid}/board").json()


def unit_of(c, cid, title):
    return next(t["unit"] for t in board(c, cid)["tasks"] if t["title"] == title)


def test_add_committee(env):
    c, cid = env
    r = c.patch(f"/api/chats/{cid}", json={"units": ["Etkinlik", "Sosyal", "Teknik", "Finans"]})
    assert r.json()["units"] == ["Etkinlik", "Sosyal", "Teknik", "Finans"]
    assert board(c, cid)["chat"]["units"][-1] == "Finans"


def test_rename_keeps_tasks(env):
    c, cid = env
    r = c.patch(f"/api/chats/{cid}", json={"renames": {"Sosyal": "İletişim"}})
    assert r.json()["units"] == ["Etkinlik", "İletişim", "Teknik"]
    assert unit_of(c, cid, "iş Sosyal") == "İletişim"
    assert unit_of(c, cid, "iş Etkinlik") == "Etkinlik"


def test_delete_moves_tasks_to_no_unit(env):
    c, cid = env
    c.patch(f"/api/chats/{cid}", json={"units": ["Sosyal", "Teknik"]})
    assert unit_of(c, cid, "iş Etkinlik") is None
    assert unit_of(c, cid, "iş Sosyal") == "Sosyal"


def test_bad_input_rejected_and_nothing_changes(env):
    c, cid = env
    for body in ({"units": ["A", "a"]}, {"units": ["A", " "]}, {"renames": {"Yok": "X"}},
                 {"renames": {"Sosyal": ""}}, {"renames": {"Sosyal": "Etkinlik"}}):
        assert c.patch(f"/api/chats/{cid}", json=body).status_code == 400, body
    assert board(c, cid)["chat"]["units"] == ["Etkinlik", "Sosyal", "Teknik"]
    assert unit_of(c, cid, "iş Sosyal") == "Sosyal"


def test_model_prompt_uses_current_units(env, monkeypatch):
    import asyncio
    from app import analyzer
    importlib.reload(analyzer)
    c, cid = env
    c.patch(f"/api/chats/{cid}", json={"renames": {"Sosyal": "İletişim"}, "units": ["Etkinlik", "İletişim"]})
    seen = []

    async def fake(msgs, *a, **k):
        seen.append(msgs[-1]["content"])
        return {}
    monkeypatch.setattr(analyzer.llm, "chat_json", fake)
    asyncio.run(analyzer.analyze(cid))
    assert seen and "UNITS: Etkinlik, İletişim" in seen[0]


def test_committee_members_saved_cleaned_and_follow_rename_and_delete(env):
    c, cid = env
    r = c.patch(f"/api/chats/{cid}", json={"unit_members": {"Etkinlik": " Ayşe Demir ,, Mert  Kaya,", "Sosyal": ""}})
    assert r.json()["unit_members"] == {"Etkinlik": "Ayşe Demir, Mert Kaya"}
    r = c.patch(f"/api/chats/{cid}", json={"unit_members": {"Teknik": "Can Yıldız"}})
    assert r.json()["unit_members"] == {"Etkinlik": "Ayşe Demir, Mert Kaya", "Teknik": "Can Yıldız"}  # others stay
    c.patch(f"/api/chats/{cid}", json={"unit_members": {"Teknik": ""}})  # blank clears one
    c.patch(f"/api/chats/{cid}", json={"renames": {"Etkinlik": "Organizasyon"}})
    assert board(c, cid)["chat"]["unit_members"] == {"Organizasyon": "Ayşe Demir, Mert Kaya"}
    c.patch(f"/api/chats/{cid}", json={"units": ["Sosyal", "Teknik"]})
    assert board(c, cid)["chat"]["unit_members"] == {}


def test_members_for_unknown_committee_rejected(env):
    c, cid = env
    assert c.patch(f"/api/chats/{cid}", json={"unit_members": {"Yok": "A"}}).status_code == 400
