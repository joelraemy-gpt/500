from __future__ import annotations

from abc import ABC, abstractmethod

from trader_agent.types import OrderRequest, OrderResult, Quote


class BrokerInterface(ABC):
    @abstractmethod
    def connect(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_account_state(self) -> dict:
        raise NotImplementedError

    @abstractmethod
    def get_quotes(self, symbols: list[str]) -> list[Quote]:
        raise NotImplementedError

    @abstractmethod
    def place_order(self, order: OrderRequest) -> OrderResult:
        raise NotImplementedError

    @abstractmethod
    def get_positions(self) -> list[dict]:
        raise NotImplementedError

    @abstractmethod
    def close_position(self, position_id: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def close_all(self) -> None:
        raise NotImplementedError
