# app/core/config.py
from pydantic import BaseModel
import os

class Settings(BaseModel):

    dnd_base: str = os.getenv("DND5E_BASE", "https://www.dnd5eapi.co/api")
    timeout: int = int(os.getenv("HTTP_TIMEOUT", "20"))
    cache_ttl_sec: int = int(os.getenv("CACHE_TTL_SEC", "3600"))

settings = Settings()