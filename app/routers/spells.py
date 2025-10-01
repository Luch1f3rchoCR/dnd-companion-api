from fastapi import APIRouter, Query, Path
from typing import Optional

router = APIRouter()

@router.get(
    "/",
    summary="List spells with filters and pagination",
    description="Returns spells from the D&D 5e SRD. Supports partial name filtering and pagination.",
    responses={
        200: {
            "description": "Spell list",
            "content": {
                "application/json": {
                    "example": {
                        "count": 2,
                        "results": [
                            {"index": "fireball", "name": "Fireball", "url": "/api/spells/fireball"},
                            {"index": "fire-bolt", "name": "Fire Bolt", "url": "/api/spells/fire-bolt"}
                        ]
                    }
                }
            }
        },
        404: {"description": "No spells found"}
    }
)
async def list_spells(
    name: Optional[str] = Query(None, description="Partial name filter. Example: fire"),
    limit: int = Query(10, ge=1, le=100, description="Maximum items per page"),
    offset: int = Query(0, ge=0, description="Items to skip for pagination")
):
    return {"count": 0, "results": []}

@router.get(
    "/{index}",
    summary="Get spell detail by index",
    description="Returns the full SRD detail of a specific spell by its index.",
    responses={
        200: {
            "description": "Spell detail",
            "content": {
                "application/json": {
                    "example": {
                        "index": "fireball",
                        "name": "Fireball",
                        "level": 3,
                        "school": {"name": "Evocation"}
                    }
                }
            }
        },
        404: {"description": "Spell not found"}
    }
)
async def get_spell(
    index: str = Path(..., description="Spell index. Example: fireball")
):
    return {"detail": "not_implemented"}