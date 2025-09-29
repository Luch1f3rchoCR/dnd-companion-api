# app/core/http_client.py
import httpx
from fastapi import HTTPException
from contextlib import asynccontextmanager

API_TIMEOUT = 15

@asynccontextmanager
async def http_client(timeout: int = API_TIMEOUT):
    """Cliente httpx con follow_redirects habilitado (para 301 de /2014/...)."""
    async with httpx.AsyncClient(timeout=timeout, follow_redirects=True) as client:
        yield client

async def fetch_json(url: str, params: dict | None = None):
    try:
        async with httpx.AsyncClient(timeout=API_TIMEOUT, follow_redirects=True) as client:
            r = await client.get(url, params=params)
            if r.status_code >= 400:
                raise HTTPException(status_code=r.status_code, detail={"upstream": r.text})
            return r.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=f"upstream_error: {e!s}")


def fetch_json_sync(url: str, params: dict | None = None):
    try:
        with httpx.Client(timeout=API_TIMEOUT, follow_redirects=True) as client:
            r = client.get(url, params=params)
            if r.status_code >= 400:
                raise HTTPException(status_code=r.status_code, detail={"upstream": r.text})
            return r.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=f"upstream_error: {e!s}")