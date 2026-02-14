from __future__ import annotations

from trader_agent.brokers.base import BrokerInterface
from trader_agent.types import OrderRequest, OrderResult, Quote


class Plus500Broker(BrokerInterface):
    """Compliance-safe stub.

    Do not implement unofficial automation or reverse-engineered APIs.
    Only wire this class if Plus500 provides an official API and the account ToS explicitly allows automation.
    """

    def connect(self) -> None:
        raise NotImplementedError("Plus500 adapter disabled: no verified official retail API integration in this project.")

    def get_account_state(self) -> dict:
        raise NotImplementedError

    def get_quotes(self, symbols: list[str]) -> list[Quote]:
        raise NotImplementedError

    def place_order(self, order: OrderRequest) -> OrderResult:
        raise NotImplementedError

    def get_positions(self) -> list[dict]:
        raise NotImplementedError

    def close_position(self, position_id: str) -> None:
        raise NotImplementedError

    def close_all(self) -> None:
        raise NotImplementedError
