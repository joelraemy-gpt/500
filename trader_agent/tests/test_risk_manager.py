from datetime import datetime, timezone

from trader_agent.risk.risk_manager import RiskManager
from trader_agent.types import Signal


def test_risk_manager_blocks_max_trades() -> None:
    rm = RiskManager(0.5, 2.0, max_trades_per_day=1, max_open_positions=5)
    rm.register_trade()
    sig = Signal("AAPL", "buy", 0.6, "test", 100, 99, 102, datetime.now(tz=timezone.utc))
    decision = rm.trade_allowed(sig, equity=100_000, open_positions=0)
    assert decision.allowed is False
    assert decision.reason == "max_trades_per_day_hit"
