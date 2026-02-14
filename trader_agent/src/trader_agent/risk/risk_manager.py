from __future__ import annotations

from dataclasses import dataclass

from trader_agent.types import Signal


@dataclass
class RiskDecision:
    allowed: bool
    reason: str
    qty: float = 0.0


class RiskManager:
    def __init__(
        self,
        risk_per_trade_pct: float,
        max_daily_loss_pct: float,
        max_trades_per_day: int,
        max_open_positions: int,
    ) -> None:
        self.risk_per_trade_pct = risk_per_trade_pct
        self.max_daily_loss_pct = max_daily_loss_pct
        self.max_trades_per_day = max_trades_per_day
        self.max_open_positions = max_open_positions
        self.trades_today = 0
        self.daily_pnl = 0.0
        self.feed_errors = 0

    def trade_allowed(self, signal: Signal, equity: float, open_positions: int) -> RiskDecision:
        if self.daily_pnl <= -(equity * self.max_daily_loss_pct / 100):
            return RiskDecision(False, "daily_loss_limit_hit")
        if self.trades_today >= self.max_trades_per_day:
            return RiskDecision(False, "max_trades_per_day_hit")
        if open_positions >= self.max_open_positions:
            return RiskDecision(False, "max_open_positions_hit")
        risk_budget = equity * (self.risk_per_trade_pct / 100)
        sl_distance = abs(signal.entry - signal.stop_loss)
        if sl_distance <= 0:
            return RiskDecision(False, "invalid_stop_loss")
        qty = max(0.0, risk_budget / sl_distance)
        return RiskDecision(True, "ok", qty=round(qty, 4))

    def register_trade(self) -> None:
        self.trades_today += 1

    def register_pnl(self, pnl: float) -> None:
        self.daily_pnl += pnl

    def register_feed_error(self) -> None:
        self.feed_errors += 1

    def circuit_breaker(self, max_errors: int) -> bool:
        return self.feed_errors >= max_errors
