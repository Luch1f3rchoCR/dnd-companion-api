from fastapi import APIRouter, Query, Path
from typing import Optional

router = APIRouter()

@router.get(
    "/",
    summary="List monsters with filters and pagination",
    description="Returns monsters from the D&D 5e SRD. Supports partial name filtering and pagination.",
    responses={
        200: {
            "description": "Monster list",
            "content": {
                "application/json": {
                    "example": {
                        "count": 2,
                        "results": [
                            {"index": "adult-black-dragon", "name": "Adult Black Dragon", "url": "/api/monsters/adult-black-dragon"},
                            {"index": "adult-blue-dragon", "name": "Adult Blue Dragon", "url": "/api/monsters/adult-blue-dragon"}
                        ]
                    }
                }
            }
        },
        404: {"description": "No monsters found"}
    }
)
async def list_monsters(
    name: Optional[str] = Query(None, description="Partial name filter. Example: dragon"),
    limit: int = Query(10, ge=1, le=100, description="Maximum items per page"),
    offset: int = Query(0, ge=0, description="Items to skip for pagination")
):
    return {"count": 0, "results": []}

@router.get(
    "/{index}",
    summary="Get monster detail by index",
    description="Returns the full SRD detail of a specific monster by its index.",
    responses={
        200: {
            "description": "Monster detail",
            "content": {
                "application/json": {
                    "example": {
                        "index": "adult-black-dragon",
                        "name": "Adult Black Dragon",
                        "size": "Huge",
                        "type": "dragon",
                        "alignment": "chaotic evil"
                    }
                }
            }
        },
        404: {"description": "Monster not found"}
    }
)
async def get_monster(
    index: str = Path(..., description="Monster index. Example: adult-black-dragon")
):
    return {"detail": "not_implemented"}