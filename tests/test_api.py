# tests/test_api.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_openapi():
    r = client.get("/openapi.json")
    assert r.status_code == 200
    j = r.json()
    assert j["info"]["title"].startswith("D&D Companion API")

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] in ("ok", "OK", "healthy") or "status" in r.json()

def test_monsters_list():
    r = client.get("/monsters", params={"limit": 3})
    assert r.status_code == 200
    j = r.json()
    assert "results" in j and isinstance(j["results"], list)
    assert j["limit"] == 3

def test_spells_search():
    r = client.get("/spells", params={"name": "fire"})
    assert r.status_code == 200
    j = r.json()
    assert any("fire" in s["name"].lower() for s in j.get("results", []))

def test_skills_proxy_list():
    r = client.get("/dnd/skills", params={"limit": 5})
    assert r.status_code == 200
    j = r.json()
    assert j["limit"] == 5
    assert len(j["results"]) <= 5

def test_feats_proxy_detail():
    # Si no habilitaste 'feats' en la whitelist, comenta este test.
    r = client.get("/dnd/feats/grappler")
    assert r.status_code == 200
    j = r.json()
    assert j["index"] == "grappler"