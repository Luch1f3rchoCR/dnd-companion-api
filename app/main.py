from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="D&D Companion API — by Luch1f3rchoCR",
    description="API pública con datos de D&D 5e. Docs en /docs y /redoc.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"],
    allow_headers=["*"], allow_credentials=True
)

@app.get("/health", tags=["meta"])
def health():
    return {"status": "ok", "version": "0.1.0"}
