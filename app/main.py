from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.routers import monsters, spells, proxy, feats, items

app = FastAPI(
    title="D&D Companion API — by Luch1f3rchoCR",
    description="Companion API for D&D 5e with filtering, pagination, caching, and interactive docs.",
    version="0.2.0",
    openapi_tags=[
        {"name": "meta", "description": "Service metadata and health"},
        {"name": "monsters", "description": "Monster listing and detail from the D&D 5e SRD"},
        {"name": "spells", "description": "Spell listing and detail from the D&D 5e SRD"},
        {"name": "feats", "description": "Feat listing and detail from the D&D 5e SRD"},
        {"name": "items", "description": "Item listing and detail from the D&D 5e SRD"},
        {"name": "dnd", "description": "Generic proxied access to allowed D&D 5e resources"}
    ],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

@app.get("/", tags=["meta"])
def root():
    return {
        "name": "D&D Companion API",
        "version": "0.2.0",
        "docs": "/docs",
        "health": "/health",
        "examples": {
            "monsters": "/monsters?name=dragon&limit=5",
            "spells": "/spells?name=fire&limit=5",
            "feats": "/feats?name=sharpshooter&limit=5",
            "items": "/items?name=sword&limit=5",
            "generic": "/dnd/monster?name=goblin&limit=5"
        }
    }

@app.get("/health", tags=["meta"])
def health():
    return {"status": "ok", "version": "0.2.0"}

@app.exception_handler(Exception)
async def unhandled(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"detail": "internal_error"})

app.include_router(monsters.router, prefix="/monsters", tags=["monsters"])
app.include_router(spells.router,   prefix="/spells",   tags=["spells"])
app.include_router(feats.router,    prefix="/feats",    tags=["feats"])
app.include_router(items.router,    prefix="/items",    tags=["items"])
app.include_router(proxy.router,    prefix="/dnd",      tags=["dnd"])