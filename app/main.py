from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.routers import monsters, spells, proxy

app = FastAPI(
    title="D&D Companion API — by Luch1f3rchoCR",
    description="Companion API sobre D&D 5e con filtros, paginación, cache y docs.",
    version="0.2.0",
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
            "monsters": "/monsters?limit=5",
            "spells": "/spells?name=fire"
        }
    }

@app.exception_handler(Exception)
async def unhandled(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"detail": "internal_error"})

@app.get("/health", tags=["meta"])
def health():
    return {"status": "ok", "version": "0.2.0"}

app.include_router(monsters.router, prefix="/monsters", tags=["monsters"])
app.include_router(spells.router,   prefix="/spells",   tags=["spells"])
app.include_router(proxy.router,    prefix="/dnd",      tags=["dnd"])