from __future__ import annotations

import random
from abc import ABC, abstractmethod
from datetime import datetime, timezone

from trader_agent.types import Quote


class MarketDataFeed(ABC):
    @abstractmethod
    def get_quotes(self, symbols: list[str]) -> list[Quote]:
        raise NotImplementedError


class MockMarketDataFeed(MarketDataFeed):
    def __init__(self) -> None:
        self._last: dict[str, float] = {}

    def get_quotes(self, symbols: list[str]) -> list[Quote]:
        out: list[Quote] = []
        now = datetime.now(tz=timezone.utc)
        for symbol in symbols:
            base = self._last.get(symbol, 100.0)
            nxt = max(1.0, base + random.uniform(-0.5, 0.5))
            self._last[symbol] = nxt
            out.append(Quote(symbol=symbol, bid=nxt - 0.01, ask=nxt + 0.01, ts=now))
        return out
