# tests/test_health.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    j = r.json()
    assert j.get("status") in ("ok", "OK", "healthy") or "status" in j