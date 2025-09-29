# app/routers/spells.py
from fastapi import APIRouter, HTTPException, Query
from app.core.config import settings
from app.core.http_client import http_client
from app.core.cache import get_ttl, set_ttl
from app.core.paging import paginate

router = APIRouter()
BASE = settings.dnd_base

@router.get("", summary="Listar hechizos (con nombre parcial y paginación)")
async def list_spells(
    name: str | None = Query(None, description="Filtro por nombre (parcial)"),
    limit: int | None = 50,
    offset: int | None = 0,
):
    cache_key = "spells:index"
    cached = get_ttl(cache_key)
    if cached is None:
        async with http_client() as client:
            r = await client.get(f"{BASE}/spells")  # <-- sin /api
            r.raise_for_status()
            cached = r.json().get("results", [])
            set_ttl(cache_key, cached, ttl_sec=3600)

    items = cached
    if name:
        items = [s for s in items if name.lower() in s["name"].lower()]

    page, limit, offset = paginate(items, limit, offset)
    return {"count": len(items), "limit": limit, "offset": offset, "results": page}

@router.get("/{index}", summary="Detalle de un hechizo por index")
async def get_spell(index: str):
    cache_key = f"spells:{index}"
    cached = get_ttl(cache_key)
    if cached is None:
        async with http_client() as client:
            r = await client.get(f"{BASE}/spells/{index}")  # <-- sin /api
            if r.status_code == 404:
                raise HTTPException(404, "Spell not found")
            r.raise_for_status()
            cached = r.json()
            set_ttl(cache_key, cached, ttl_sec=3600)
    return cached