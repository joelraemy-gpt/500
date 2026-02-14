from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Literal


Direction = Literal["buy", "sell"]


@dataclass(slots=True)
class Signal:
    symbol: str
    direction: Direction
    confidence: float
    rationale: str
    entry: float
    stop_loss: float
    take_profit: float
    ts: datetime


@dataclass(slots=True)
class OrderRequest:
    symbol: str
    side: Direction
    qty: float
    order_type: str = "market"
    stop_loss: float | None = None
    take_profit: float | None = None


@dataclass(slots=True)
class OrderResult:
    order_id: str
    status: str
    fill_price: float
    filled_qty: float
    commission: float


@dataclass(slots=True)
class Quote:
    symbol: str
    bid: float
    ask: float
    ts: datetime
