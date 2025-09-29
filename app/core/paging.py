from typing import Sequence

def paginate(seq: Sequence, limit: int | None, offset: int | None):
    limit = max(1, min(limit or 50, 200))
    offset = max(0, offset or 0)
    return seq[offset: offset + limit], limit, offset