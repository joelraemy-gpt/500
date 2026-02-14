from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime, timezone

from trader_agent.brokers.base import BrokerInterface
from trader_agent.types import OrderRequest, OrderResult, Quote


@dataclass
class Position:
    id: str
    symbol: str
    side: str
    qty: float
    entry_price: float


class PaperBroker(BrokerInterface):
    def __init__(self, initial_equity: float, commission_per_trade: float, slippage_bps: float) -> None:
        self.initial_equity = initial_equity
        self.cash = initial_equity
        self.commission_per_trade = commission_per_trade
        self.slippage_bps = slippage_bps
        self.positions: dict[str, Position] = {}
        self._last_quotes: dict[str, Quote] = {}

    def connect(self) -> None:
        return

    def update_quotes(self, quotes: list[Quote]) -> None:
        for q in quotes:
            self._last_quotes[q.symbol] = q

    def get_account_state(self) -> dict:
        exposure = sum(p.qty * p.entry_price for p in self.positions.values())
        return {"cash": self.cash, "equity": self.cash + exposure, "open_positions": len(self.positions)}

    def get_quotes(self, symbols: list[str]) -> list[Quote]:
        return [self._last_quotes[s] for s in symbols if s in self._last_quotes]

    def place_order(self, order: OrderRequest) -> OrderResult:
        quote = self._last_quotes[order.symbol]
        base = quote.ask if order.side == "buy" else quote.bid
        fill_price = base * (1 + self.slippage_bps / 10_000 if order.side == "buy" else 1 - self.slippage_bps / 10_000)
        notional = order.qty * fill_price
        order_id = str(uuid.uuid4())

        if order.side == "buy":
            self.cash -= notional + self.commission_per_trade
            pid = str(uuid.uuid4())
            self.positions[pid] = Position(pid, order.symbol, order.side, order.qty, fill_price)
        else:
            self.cash += notional - self.commission_per_trade
        return OrderResult(
            order_id=order_id,
            status="filled",
            fill_price=fill_price,
            filled_qty=order.qty,
            commission=self.commission_per_trade,
        )

    def get_positions(self) -> list[dict]:
        return [p.__dict__ for p in self.positions.values()]

    def close_position(self, position_id: str) -> None:
        if position_id not in self.positions:
            return
        pos = self.positions.pop(position_id)
        quote = self._last_quotes[pos.symbol]
        exit_price = quote.bid
        self.cash += pos.qty * exit_price - self.commission_per_trade

    def close_all(self) -> None:
        for pid in list(self.positions.keys()):
            self.close_position(pid)
