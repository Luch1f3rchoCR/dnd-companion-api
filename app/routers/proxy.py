from typing import Optional, Literal, Dict, Any, List
from fastapi import APIRouter, Query, Path, HTTPException
import httpx
import asyncio

router = APIRouter()

AllowedResource = Literal["monster", "spell", "feat", "item"]

BASES = {
    "monster": "https://www.dnd5eapi.co/api/monsters",
    "spell":   "https://www.dnd5eapi.co/api/spells",
    "feat":    "https://www.dnd5eapi.co/api/feats",
    "item":    "https://www.dnd5eapi.co/api/equipment",
}
CATEGORIES = "https://www.dnd5eapi.co/api/equipment-categories"
ROOT = "https://www.dnd5eapi.co"

async def fetch_json(client: httpx.AsyncClient, url: str) -> Dict[str, Any]:
    r = await client.get(url, timeout=20)
    if r.status_code == 404:
        raise HTTPException(status_code=404, detail="not_found")
    r.raise_for_status()
    return r.json()

@router.get(
    "/{resource}",
    summary="Generic D&D SRD listing",
    description=(
        "Generic proxied listing for allowed resources (monster, spell, feat, item). "
        "Supports partial name filtering, pagination, and `expand=true` to return full detail. "
        "For `item`, you may pass `category` (e.g. weapon, armor, adventuring-gear) to list by equipment category."
    ),
    responses={
        200: {
            "description": "List result",
            "content": {
                "application/json": {
                    "example": {
                        "count": 2,
                        "results": [
                            {"index": "goblin", "name": "Goblin", "url": "/api/monsters/goblin"},
                            {"index": "goblin-boss", "name": "Goblin Boss", "url": "/api/monsters/goblin-boss"}
                        ]
                    }
                }
            }
        },
        404: {"description": "No results found or invalid category"},
    }
)
async def generic_list(
    resource: AllowedResource = Path(..., description="Allowed: monster, spell, feat, item"),
    name: Optional[str] = Query(None, description="Partial case-insensitive name filter"),
    limit: int = Query(10, ge=1, le=100, description="Max items per page"),
    offset: int = Query(0, ge=0, description="Pagination offset"),
    expand: bool = Query(False, description="Fetch full record for each item"),
    category: Optional[str] = Query(None, description="Only for resource=item: SRD equipment category index")
):
    base = BASES[resource]

    async with httpx.AsyncClient(limits=httpx.Limits(max_keepalive_connections=8, max_connections=16)) as client:
        if resource == "item" and category:
            data = await fetch_json(client, f"{CATEGORIES}/{category}")
            raw = data.get("equipment", [])
        else:
            data = await fetch_json(client, base)
            raw = data.get("results", [])

        if name:
            q = name.lower()
            raw = [r for r in raw if q in r.get("name", "").lower()]

        count = len(raw)
        page = raw[offset : offset + limit]

        if not expand:
            return {"count": count, "results": page}

        urls = [ROOT + r["url"] for r in page if "url" in r]
        tasks = [fetch_json(client, u) for u in urls]
        details: List[Dict[str, Any]] = await asyncio.gather(*tasks)
        return {"count": count, "results": details}