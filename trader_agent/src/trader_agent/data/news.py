from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime, timezone


class NewsProviderInterface(ABC):
    @abstractmethod
    def get_events(self) -> list[dict]:
        raise NotImplementedError


class EconomicCalendarProviderInterface(ABC):
    @abstractmethod
    def get_events(self) -> list[dict]:
        raise NotImplementedError


class StubNewsProvider(NewsProviderInterface):
    def get_events(self) -> list[dict]:
        return [{"source": "stub", "headline": "No significant events", "confidence": 0.1, "ts": datetime.now(tz=timezone.utc)}]


class StubEconomicCalendar(EconomicCalendarProviderInterface):
    def get_events(self) -> list[dict]:
        return []
