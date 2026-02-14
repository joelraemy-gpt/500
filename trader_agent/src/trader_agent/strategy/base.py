from __future__ import annotations

from abc import ABC, abstractmethod

from trader_agent.types import Quote, Signal


class StrategyInterface(ABC):
    @abstractmethod
    def on_tick(self, quote: Quote) -> Signal | None:
        raise NotImplementedError

    @abstractmethod
    def on_bar(self, symbol: str, close: float) -> Signal | None:
        raise NotImplementedError

    @abstractmethod
    def on_news_event(self, event: dict) -> Signal | None:
        raise NotImplementedError
