from __future__ import annotations

import time
from collections.abc import Callable


class TTLCache:
    def __init__(self, ttl_seconds: int) -> None:
        self.ttl_seconds = ttl_seconds
        self._store: dict[str, tuple[float, object]] = {}

    def get_or_set(self, key: str, factory: Callable[[], object]) -> object:
        now = time.time()
        if key in self._store:
            ts, val = self._store[key]
            if now - ts < self.ttl_seconds:
                return val
        val = factory()
        self._store[key] = (now, val)
        return val
