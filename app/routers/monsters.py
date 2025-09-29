# app/routers/monsters.py
from fastapi import APIRouter, HTTPException, Query
import httpx

BASE = "https://www.dnd5eapi.co"
router = APIRouter()

@router.get("", summary="Listar monstruos con filtros")
async def list_monsters(
    name: str | None = Query(None, description="Nombre (parcial)"),
    type: str | None = Query(None, description="Aberration, Dragon, Undead, etc."),
    cr_min: float | None = Query(None, description="CR mínimo"),
    cr_max: float | None = Query(None, description="CR máximo"),
):
    async with httpx.AsyncClient(timeout=20) as client:
        idx = await client.get(f"{BASE}/api/monsters")
        idx.raise_for_status()
        items = idx.json().get("results", [])

        if name:
            items = [m for m in items if name.lower() in m["name"].lower()]

        need_expand = bool(type or cr_min is not None or cr_max is not None)
        if need_expand:
            expanded = []
            for m in items[:40]:  # límite demo
                r = await client.get(f"{BASE}{m['url']}")
                if r.is_success:
                    md = r.json()
                    expanded.append({
                        "name": md.get("name"),
                        "type": md.get("type"),
                        "challenge_rating": md.get("challenge_rating"),
                        "size": md.get("size"),
                        "alignment": md.get("alignment"),
                    })
            items = expanded
            if type:
                items = [m for m in items if str(m.get("type","")).lower() == type.lower()]
            if cr_min is not None:
                items = [m for m in items if (m.get("challenge_rating") or 0) >= cr_min]
            if cr_max is not None:
                items = [m for m in items if (m.get("challenge_rating") or 0) <= cr_max]

        return {"count": len(items), "results": items}

@router.get("/{index}", summary="Detalle por index")
async def get_monster(index: str):
    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.get(f"{BASE}/api/monsters/{index}")
        if r.status_code == 404:
            raise HTTPException(status_code=404, detail="Monster not found")
        r.raise_for_status()
        md = r.json()
        return {
            "name": md.get("name"),
            "type": md.get("type"),
            "size": md.get("size"),
            "alignment": md.get("alignment"),
            "challenge_rating": md.get("challenge_rating"),
            "hit_points": md.get("hit_points"),
            "armor_class": md.get("armor_class"),
            "languages": md.get("languages"),
            "actions": md.get("actions"),
        }