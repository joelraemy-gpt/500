from __future__ import annotations

import logging
import time

import typer

from trader_agent.brokers.paper import PaperBroker
from trader_agent.config import settings
from trader_agent.data.market_data import MockMarketDataFeed
from trader_agent.execution.order_manager import OrderManager
from trader_agent.execution.position_manager import PositionManager
from trader_agent.logging_setup import setup_logging
from trader_agent.monitoring.health import health_report
from trader_agent.risk.risk_manager import RiskManager
from trader_agent.storage.db import Storage
from trader_agent.strategy.examples import MovingAverageCrossoverStrategy

app = typer.Typer(help="Trading agent CLI")
logger = logging.getLogger(__name__)


def build_components() -> tuple[PaperBroker, MockMarketDataFeed, MovingAverageCrossoverStrategy, RiskManager, Storage]:
    broker = PaperBroker(settings.paper_initial_equity, settings.paper_commission_per_trade, settings.paper_slippage_bps)
    feed = MockMarketDataFeed()
    strategy = MovingAverageCrossoverStrategy()
    risk = RiskManager(
        risk_per_trade_pct=settings.risk_per_trade_pct,
        max_daily_loss_pct=settings.max_daily_loss_pct,
        max_trades_per_day=settings.max_trades_per_day,
        max_open_positions=settings.max_open_positions,
    )
    storage = Storage(settings.db_url)
    storage.init()
    return broker, feed, strategy, risk, storage


@app.command()
def paper(symbols: str = "AAPL,MSFT", iterations: int = 20) -> None:
    """Run paper-trading loop (default-safe mode)."""
    setup_logging(settings.log_level, settings.log_json)
    broker, feed, strategy, risk, storage = build_components()
    broker.connect()
    position_mgr = PositionManager()
    order_mgr = OrderManager(broker)

    sym_list = [s.strip().upper() for s in symbols.split(",") if s.strip()]
    for _ in range(iterations):
        quotes = feed.get_quotes(sym_list)
        broker.update_quotes(quotes)
        position_mgr.sync(broker.get_positions())
        account = broker.get_account_state()

        for q in quotes:
            sig = strategy.on_tick(q)
            if not sig:
                continue
            storage.add_signal(sig.symbol, sig.direction, sig.confidence, sig.rationale)
            decision = risk.trade_allowed(sig, equity=account["equity"], open_positions=position_mgr.count())
            storage.add_decision(decision.allowed, decision.reason)
            if not decision.allowed:
                continue
            order = order_mgr.execute_signal(sig, decision.qty)
            risk.register_trade()
            storage.add_order(order["order_id"], sig.symbol, sig.direction, order["qty"], order["fill_price"], order["status"])

        if risk.circuit_breaker(settings.circuit_breaker_feed_errors):
            logger.warning("circuit_breaker_triggered")
            break
        time.sleep(settings.loop_sleep_seconds)

    typer.echo("paper run complete")


@app.command()
def status() -> None:
    setup_logging(settings.log_level, settings.log_json)
    broker, _, _, _, _ = build_components()
    report = health_report(feed_ok=True, broker_ok=True, latency_ms=20)
    typer.echo(f"status={report['status']} account={broker.get_account_state()}")


@app.command("kill-switch")
def kill_switch(close_positions: bool = False) -> None:
    setup_logging(settings.log_level, settings.log_json)
    broker, _, _, _, _ = build_components()
    if close_positions:
        broker.close_all()
    typer.echo("kill-switch engaged: engine stopped")


@app.command()
def live() -> None:
    if not settings.live_trading:
        raise typer.BadParameter("LIVE_TRADING=false. Live mode requires explicit opt-in.")
    typer.echo("Live mode skeleton ready. Use compliant broker adapter only.")


@app.command()
def backtest(symbol: str, from_date: str, to_date: str) -> None:
    typer.echo(f"backtest stub: {symbol} {from_date} -> {to_date}")


if __name__ == "__main__":
    app()
