from __future__ import annotations


class SimpleMetrics:
    def __init__(self) -> None:
        self.counters: dict[str, int] = {}

    def inc(self, key: str, by: int = 1) -> None:
        self.counters[key] = self.counters.get(key, 0) + by
