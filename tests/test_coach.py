import importlib

import pytest
from fastapi.testclient import TestClient

CHAT = "17.10.2026 19:33 - Ayşe: gizli sohbet cümlesi 777\n17.10.2026 19:34 - Mert: tamam\n"


@pytest.fixture()
def env(tmp_path, monkeypatch):
    monkeypatch.setenv("PANO_DB", str(tmp_path / "c.db"))
    from app import db
    db._conn = None
    importlib.reload(db)
    from app import coach, main
    importlib.reload(coach)
    importlib.reload(main)
    c = TestClient(main.app)
    cid = c.post("/api/chats?units=Etkinlik,Sponsorluk", content=CHAT.encode()).json()["id"]
    t = c.post(f"/api/chats/{cid}/items", json={"title": "Afiş tasarla", "due": "2020-01-01", "unit": "Etkinlik"}).json()
    return c, cid, t["id"], coach


def test_week_plan_keeps_only_steps_tied_to_a_record_or_team_and_is_saved(env, monkeypatch):
    c, cid, tid, coach = env
    seen = []

    async def chat_json(messages, schema, **k):
        seen.append(messages[0]["content"])
        return {"steps": [
            {"action": "Afişi bitir", "why": "Süresi geçti.", "ref": f"[T{tid}]", "unit": "Etkinlik", "owner": "Ayşe", "when": "2026-10-19"},
            {"action": "Uydurma iş", "why": "x", "ref": "T9999", "unit": "", "owner": "", "when": ""},
            {"action": "Sponsorluk toplansın", "why": "y", "ref": "", "unit": "Sponsorluk", "owner": "Kimse Yok", "when": ""},
            {"action": "Sahipsiz adım", "why": "z", "ref": "", "unit": "", "owner": "", "when": ""}]}
    monkeypatch.setattr(coach.llm, "chat_json", chat_json)
    r = c.post(f"/api/chats/{cid}/week").json()
    assert [s["action"] for s in r["steps"]] == ["Afişi bitir", "Sponsorluk toplansın"] or \
           [s["action"] for s in r["steps"]] == ["Sponsorluk toplansın", "Afişi bitir"]
    assert f"[T{tid}] Afiş tasarla" in seen[0] and "gizli sohbet" not in seen[0]
    assert all(s["owner"] in (None, "Ayşe") for s in r["steps"])
    assert len(c.get(f"/api/chats/{cid}/saved/week").json()["saved"]) == 1


def test_week_plan_with_nothing_open_does_not_call_the_model(env, monkeypatch):
    c, cid, tid, coach = env
    c.patch(f"/api/items/{tid}", json={"status": "done"})

    async def boom(*a, **k):
        raise AssertionError("model must not be called")
    monkeypatch.setattr(coach.llm, "chat_json", boom)
    assert c.post(f"/api/chats/{cid}/week").json()["reason"] == "nothing_open"


def test_handover_rejects_invented_figures_and_saves_a_checked_one(env, monkeypatch):
    c, cid, tid, coach = env
    answers = iter(["Genel görünüm\n1 görev var, 888 kişi geldi.", "Genel görünüm\n1 görev var, 888 kişi geldi.",
                    "Genel görünüm\n1 görev var."])

    async def chat(messages, *a, **k):
        return next(answers)
    monkeypatch.setattr(coach.llm, "chat", chat)
    r = c.post(f"/api/chats/{cid}/handover")
    assert r.status_code == 422 and "888" in r.json()["detail"]["unsupported"]
    assert c.get(f"/api/chats/{cid}/saved/handover").json()["saved"] == []
    r = c.post(f"/api/chats/{cid}/handover")
    assert r.status_code == 200 and "888" not in r.json()["text"]
    saved = c.get(f"/api/chats/{cid}/saved/handover").json()["saved"]
    assert len(saved) == 1 and c.delete(f"/api/saved/{saved[0]['id']}").status_code == 200


def test_weekly_report_page_shows_records_and_saved_roadmap(env, monkeypatch):
    c, cid, tid, coach = env

    async def chat_json(messages, schema, **k):
        return {"assessment": "Bir görev gecikti.", "agenda": ["Afişi konuş"],
                "steps": [{"action": "Afişi bitir", "why": "Süresi geçti.", "ref": f"T{tid}", "unit": "Etkinlik", "owner": "", "when": ""}]}
    monkeypatch.setattr(coach.llm, "chat_json", chat_json)
    page = c.get(f"/api/chats/{cid}/weekly-report").text
    assert "Afiş tasarla" in page and "Henüz haftalık yol haritası" in page   # records show even before the model ran
    c.post(f"/api/chats/{cid}/week")
    page = c.get(f"/api/chats/{cid}/weekly-report").text
    assert "Afişi bitir" in page and "Bir görev gecikti." in page and "Afişi konuş" in page and "gemma" in page.lower()
