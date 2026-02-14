from __future__ import annotations

from collections import defaultdict, deque
from datetime import datetime, timezone

from trader_agent.strategy.base import StrategyInterface
from trader_agent.types import Quote, Signal


class MovingAverageCrossoverStrategy(StrategyInterface):
    """Toy strategy for demonstration/testing only."""

    def __init__(self, short_window: int = 3, long_window: int = 5) -> None:
        self.short_window = short_window
        self.long_window = long_window
        self.prices: dict[str, deque[float]] = defaultdict(lambda: deque(maxlen=self.long_window))

    def _signal_for(self, symbol: str) -> Signal | None:
        buf = self.prices[symbol]
        if len(buf) < self.long_window:
            return None
        short_ma = sum(list(buf)[-self.short_window:]) / self.short_window
        long_ma = sum(buf) / self.long_window
        px = buf[-1]
        if short_ma > long_ma:
            return Signal(symbol, "buy", 0.6, "toy_ma_cross_up", px, px * 0.99, px * 1.02, datetime.now(tz=timezone.utc))
        if short_ma < long_ma:
            return Signal(symbol, "sell", 0.6, "toy_ma_cross_down", px, px * 1.01, px * 0.98, datetime.now(tz=timezone.utc))
        return None

    def on_tick(self, quote: Quote) -> Signal | None:
        self.prices[quote.symbol].append((quote.bid + quote.ask) / 2)
        return self._signal_for(quote.symbol)

    def on_bar(self, symbol: str, close: float) -> Signal | None:
        self.prices[symbol].append(close)
        return self._signal_for(symbol)

    def on_news_event(self, event: dict) -> Signal | None:
        return None
