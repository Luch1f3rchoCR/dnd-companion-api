# app/routers/proxy.py
from fastapi import APIRouter, HTTPException, Query
from app.core.config import settings
from app.core.http_client import http_client
from app.core.cache import get_ttl, set_ttl
from app.core.paging import paginate

router = APIRouter()
BASE = settings.dnd_base

ALLOW = {
    "ability-scores","alignments","backgrounds","classes","conditions",
    "damage-types","equipment","equipment-categories","features","languages",
    "magic-items","magic-schools","monsters","proficiencies","races",
    "skills","spells","subclasses","subraces","traits","weapon-properties",
    "feats"
}

@router.get("/{resource}", summary="Listado genérico de un recurso permitido")
async def list_resource(resource: str,
    name: str | None = Query(None, description="Filtro por nombre parcial"),
    limit: int | None = 50, offset: int | None = 0):
    if resource not in ALLOW:
        raise HTTPException(400, "Recurso no permitido")
    cache_key = f"{resource}:index"
    data = get_ttl(cache_key)
    if data is None:
        async with http_client() as client:
            r = await client.get(f"{BASE}/{resource}")  # <-- sin /api
            r.raise_for_status()
            data = r.json().get("results", [])
            set_ttl(cache_key, data, ttl_sec=3600)
    items = data
    if name:
        items = [i for i in items if name.lower() in i["name"].lower()]
    page, limit, offset = paginate(items, limit, offset)
    return {"count": len(items), "limit": limit, "offset": offset, "results": page}

@router.get("/{resource}/{index}", summary="Detalle genérico por index")
async def get_resource(resource: str, index: str):
    if resource not in ALLOW:
        raise HTTPException(400, "Recurso no permitido")
    cache_key = f"{resource}:{index}"
    doc = get_ttl(cache_key)
    if doc is None:
        async with http_client() as client:
            r = await client.get(f"{BASE}/{resource}/{index}")  # <-- sin /api
            if r.status_code == 404:
                raise HTTPException(404, "No encontrado")
            r.raise_for_status()
            doc = r.json()
            set_ttl(cache_key, doc, ttl_sec=3600)
    return doc