from __future__ import annotations


class PositionManager:
    def __init__(self) -> None:
        self._positions: dict[str, dict] = {}

    def sync(self, broker_positions: list[dict]) -> None:
        self._positions = {p["id"]: p for p in broker_positions}

    def count(self) -> int:
        return len(self._positions)

    def all(self) -> list[dict]:
        return list(self._positions.values())
