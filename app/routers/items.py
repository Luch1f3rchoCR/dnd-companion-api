from typing import Optional, Literal, List, Dict, Any
from fastapi import APIRouter, Query
import httpx

router = APIRouter()

BaseURL = "https://www.dnd5eapi.co"

SimpleCategory = Literal[
    "weapon",
    "armor",
    "adventuring-gear",
    "tools",
    "potion",
    "ammunition"
]

AliasCategory = Literal[
    "sword",
    "axe",
    "bow",
    "shield",
    "light-armor",
    "medium-armor",
    "heavy-armor"
]

SupportedCategory = Literal[
    "weapon",
    "armor",
    "adventuring-gear",
    "tools",
    "potion",
    "ammunition",
    "sword",
    "axe",
    "bow",
    "shield",
    "light-armor",
    "medium-armor",
    "heavy-armor"
]

async def fetch_json(client: httpx.AsyncClient, path: str) -> Dict[str, Any]:
    r = await client.get(f"{BaseURL}{path}", timeout=20)
    r.raise_for_status()
    return r.json()

def apply_name_filter(rows: List[Dict[str, Any]], name: Optional[str]) -> List[Dict[str, Any]]:
    if not name:
        return rows
    needle = name.lower()
    return [x for x in rows if needle in x.get("name", "").lower()]

def alias_filter(rows: List[Dict[str, Any]], alias: AliasCategory) -> List[Dict[str, Any]]:
    if alias == "sword":
        return [x for x in rows if "sword" in x.get("name", "").lower()]
    if alias == "axe":
        return [x for x in rows if "axe" in x.get("name", "").lower()]
    if alias == "bow":
        return [x for x in rows if "bow" in x.get("name", "").lower()]
    if alias == "shield":
        return [x for x in rows if "shield" in x.get("name", "").lower()]
    if alias in {"light-armor", "medium-armor", "heavy-armor"}:
        key = alias.replace("-armor", "")
        return [x for x in rows if key in x.get("name", "").lower()]
    return rows

@router.get(
    "",
    summary="List items with name and category filters",
    description="Search D&D 5e equipment by partial name and category. Uses SRD equipment categories for coarse filtering and text matching for aliases like sword or shield.",
    responses={
        200: {"description": "Item list"},
        502: {"description": "Upstream SRD error"}
    }
)
async def list_items(
    name: Optional[str] = Query(None, description="Partial name filter (e.g. sword)"),
    category: Optional[SupportedCategory] = Query(
        None,
        description="One of: weapon, armor, adventuring-gear, tools, potion, ammunition, sword, axe, bow, shield, light-armor, medium-armor, heavy-armor"
    ),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    async with httpx.AsyncClient() as client:
        rows: List[Dict[str, Any]] = []

        if category in {"weapon", "armor", "adventuring-gear", "tools", "potion", "ammunition"}:
            data = await fetch_json(client, f"/api/equipment-categories/{category}")
            rows = data.get("equipment", [])
        else:
            data = await fetch_json(client, "/api/equipment")
            rows = data.get("results", [])

        if isinstance(category, str) and category in {"sword", "axe", "bow", "shield", "light-armor", "medium-armor", "heavy-armor"}:
            rows = alias_filter(rows, category)  # type: ignore[arg-type]

        rows = apply_name_filter(rows, name)
        total = len(rows)
        page = rows[offset: offset + limit]

        return {"count": total, "results": page}

@router.get(
    "/categories",
    summary="List supported item categories",
    description="Returns the accepted values for the category filter."
)
def supported_categories():
    return {
        "simple": ["weapon", "armor", "adventuring-gear", "tools", "potion", "ammunition"],
        "aliases": ["sword", "axe", "bow", "shield", "light-armor", "medium-armor", "heavy-armor"]
    }