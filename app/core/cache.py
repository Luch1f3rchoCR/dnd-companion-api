import time
from typing import Any, Optional

_store: dict[str, tuple[float, Any]] = {}

def set_ttl(key: str, value: Any, ttl_sec: int) -> None:
    _store[key] = (time.time() + ttl_sec, value)

def get_ttl(key: str) -> Optional[Any]:
    exp_val = _store.get(key)
    if not exp_val:
        return None
    exp, val = exp_val
    if time.time() > exp:
        _store.pop(key, None)
        return None
    return val