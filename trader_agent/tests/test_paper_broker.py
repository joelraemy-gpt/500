from datetime import datetime, timezone

from trader_agent.brokers.paper import PaperBroker
from trader_agent.types import OrderRequest, Quote


def test_paper_broker_fill_simulation() -> None:
    b = PaperBroker(initial_equity=10000, commission_per_trade=1, slippage_bps=10)
    b.update_quotes([Quote(symbol="AAPL", bid=100, ask=100.1, ts=datetime.now(tz=timezone.utc))])
    res = b.place_order(OrderRequest(symbol="AAPL", side="buy", qty=1))
    assert res.status == "filled"
    assert res.fill_price > 100.1
