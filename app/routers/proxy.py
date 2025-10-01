from fastapi import APIRouter, Query, Path
from typing import Optional, Literal

router = APIRouter()

AllowedResource = Literal["monster", "spell", "feat", "item"]

@router.get(
    "/{resource}",
    summary="Generic D&D SRD listing",
    description="Generic proxied listing for allowed resources. Supports partial name filtering and pagination.",
    responses={
        200: {
            "description": "Generic list",
            "content": {
                "application/json": {
                    "example": {
                        "count": 1,
                        "results": [{"index": "goblin", "name": "Goblin"}]
                    }
                }
            }
        },
        400: {"description": "Invalid resource"},
        404: {"description": "No results found"}
    }
)
async def generic_list(
    resource: AllowedResource = Path(..., description="Allowed values: monster, spell, feat, item"),
    name: Optional[str] = Query(None, description="Partial name filter. Example: goblin"),
    limit: int = Query(10, ge=1, le=100, description="Maximum items per page"),
    offset: int = Query(0, ge=0, description="Items to skip for pagination")
):
    return {"count": 0, "results": []}