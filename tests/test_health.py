import asyncio, httpx

def test_health():

    r = httpx.get("http://127.0.0.1:8000/health", timeout=10)
    assert r.status_code == 200
    assert r.json()["status"] == "ok"