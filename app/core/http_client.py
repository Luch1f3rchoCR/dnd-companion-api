import httpx
from app.core.config import settings


def http_client() -> httpx.AsyncClient:
    return httpx.AsyncClient(timeout=settings.timeout)