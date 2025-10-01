from fastapi import APIRouter, Query, Path
from typing import Optional

router = APIRouter()

@router.get(
    "/",
    summary="List feats with filters and pagination",
    description="Returns feats from the D&D 5e SRD. Supports partial name filtering and pagination.",
    responses={
        200: {
            "description": "Feat list",
            "content": {
                "application/json": {
                    "example": {
                        "count": 2,
                        "results": [
                            {"index": "grappler", "name": "Grappler"},
                            {"index": "sharpshooter", "name": "Sharpshooter"}
                        ]
                    }
                }
            }
        },
        404: {"description": "No feats found"}
    }
)
async def list_feats(
    name: Optional[str] = Query(None, description="Partial name filter. Example: sharpshooter"),
    limit: int = Query(10, ge=1, le=100, description="Maximum items per page"),
    offset: int = Query(0, ge=0, description="Items to skip for pagination")
):
    return {"count": 0, "results": []}

@router.get(
    "/{index}",
    summary="Get feat detail by index",
    description="Returns the full SRD detail of a specific feat by its index.",
    responses={
        200: {
            "description": "Feat detail",
            "content": {
                "application/json": {
                    "example": {
                        "index": "sharpshooter",
                        "name": "Sharpshooter"
                    }
                }
            }
        },
        404: {"description": "Feat not found"}
    }
)
async def get_feat(
    index: str = Path(..., description="Feat index. Example: sharpshooter")
):
    return {"detail": "not_implemented"}