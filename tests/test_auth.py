import importlib

import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("PANO_DB", str(tmp_path / "a.db"))
    monkeypatch.setenv("PANO_AUTH", "1")
    from app import db
    db._conn = None
    importlib.reload(db)
    from app import auth, main
    importlib.reload(auth)
    importlib.reload(main)
    with TestClient(main.app) as c:
        yield c


def test_api_needs_sign_in_but_health_and_auth_do_not(client):
    assert client.get("/api/chats").status_code == 401
    assert client.get("/api/health").status_code == 200
    me = client.get("/api/auth/me").json()
    assert me["user"] is None and me["can_register"] is True


def test_register_login_logout_cycle(client):
    assert client.post("/api/auth/register", json={"username": "ab", "password": "123456"}).status_code == 400
    assert client.post("/api/auth/register", json={"username": "baskan", "password": "gizli123"}).status_code == 200
    assert client.get("/api/chats").status_code == 200                      # cookie from register
    assert client.post("/api/auth/register", json={"username": "baska", "password": "gizli123"}).status_code == 403
    client.post("/api/auth/logout")
    assert client.get("/api/chats").status_code == 401
    assert client.post("/api/auth/login", json={"username": "baskan", "password": "yanlis!"}).status_code == 401
    assert client.post("/api/auth/login", json={"username": "BASKAN", "password": "gizli123"}).status_code == 200
    assert client.get("/api/auth/me").json()["user"] == "BASKAN" or client.get("/api/auth/me").json()["user"]
