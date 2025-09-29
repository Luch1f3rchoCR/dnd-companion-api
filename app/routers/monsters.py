# app/routers/monsters.py
from fastapi import APIRouter, HTTPException, Query
import httpx
from typing import Any, Dict, List, Optional
import time, os
from urllib.parse import urljoin

API_BASE = os.getenv("API_BASE", "https://www.dnd5eapi.co/api").rstrip("/") + "/"
router = APIRouter()

_CACHE: Dict[str, tuple[float, Any]] = {}

def cache_get(key: str) -> Optional[Any]:
    v = _CACHE.get(key)
    if not v:
        return None
    exp, data = v
    if time.time() > exp:
        _CACHE.pop(key, None)
        return None
    return data

def cache_set(key: str, value: Any, ttl_sec: int = 3600) -> None:
    _CACHE[key] = (time.time() + ttl_sec, value)

ALLOWED_TYPES = {
    "aberration","beast","celestial","construct","dragon","elemental","fey",
    "fiend","giant","humanoid","monstrosity","ooze","plant","undead","swarm of tiny beasts"
}

@router.get("", summary="List monsters with filters & pagination", tags=["monsters"])
async def list_monsters(
    name: str | None = Query(None),
    type: str | None = Query(None),
    cr_min: float | None = Query(None),
    cr_max: float | None = Query(None),
    limit: int | None = Query(50, ge=1, le=200),
    offset: int | None = Query(0, ge=0),
):
    idx_key = "monsters:index"
    items: List[Dict[str, Any]] = cache_get(idx_key) or []
    if not items:
        async with httpx.AsyncClient(timeout=20, follow_redirects=True) as client:
            r = await client.get(urljoin(API_BASE, "monsters"))
            r.raise_for_status()
            items = r.json().get("results", [])
            cache_set(idx_key, items, 3600)

    if name:
        items = [m for m in items if name.lower() in m["name"].lower()]

    need_expand = bool(type or cr_min is not None or cr_max is not None)
    if need_expand:
        type_norm = type.lower() if type else None
        expanded: List[Dict[str, Any]] = []
        async with httpx.AsyncClient(timeout=20, follow_redirects=True) as client:
            for m in items[:50]:
                try:

                    path = m["url"].lstrip("/")
                    r = await client.get(urljoin(API_BASE, path))
                    if not r.is_success:
                        continue
                    md = r.json()
                    expanded.append({
                        "name": md.get("name"),
                        "type": (md.get("type") or "").lower() if md.get("type") else None,
                        "challenge_rating": md.get("challenge_rating"),
                        "size": md.get("size"),
                        "alignment": md.get("alignment"),
                    })
                except Exception:
                    continue
        if type_norm:
            expanded = [m for m in expanded if (m.get("type") or "") == type_norm]
        if cr_min is not None:
            expanded = [m for m in expanded if (m.get("challenge_rating") or 0) >= cr_min]
        if cr_max is not None:
            expanded = [m for m in expanded if (m.get("challenge_rating") or 0) <= cr_max]
        items = expanded

    lim = max(1, min(limit or 50, 200))
    off = max(0, offset or 0)
    page = items[off: off + lim]
    return {"count": len(items), "limit": lim, "offset": off, "results": page}

@router.get("/{index}", summary="Monster detail by index", tags=["monsters"])
async def get_monster(index: str):
    cache_key = f"monsters:{index}"
    cached = cache_get(cache_key)
    if cached:
        return cached
    async with httpx.AsyncClient(timeout=20, follow_redirects=True) as client:
        r = await client.get(urljoin(API_BASE, f"monsters/{index}"))
        if r.status_code == 404:
            raise HTTPException(404, "Monster not found")
        r.raise_for_status()
        md = r.json()
        doc = {
            "name": md.get("name"),
            "type": md.get("type"),
            "size": md.get("size"),
            "alignment": md.get("alignment"),
            "challenge_rating": md.get("challenge_rating"),
            "hit_points": md.get("hit_points"),
            "armor_class": md.get("armor_class"),
            "languages": md.get("languages"),
            "proficiencies": md.get("proficiencies"),
            "actions": md.get("actions"),
        }
        cache_set(cache_key, doc, 3600)
        return doc