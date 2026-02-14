from __future__ import annotations

import logging

from trader_agent.brokers.base import BrokerInterface
from trader_agent.types import OrderRequest, Signal


class OrderManager:
    def __init__(self, broker: BrokerInterface) -> None:
        self.broker = broker
        self.logger = logging.getLogger(__name__)

    def execute_signal(self, signal: Signal, qty: float) -> dict:
        req = OrderRequest(
            symbol=signal.symbol,
            side=signal.direction,
            qty=qty,
            stop_loss=signal.stop_loss,
            take_profit=signal.take_profit,
        )
        result = self.broker.place_order(req)
        self.logger.info("order_executed", extra={"correlation_id": result.order_id})
        return {
            "order_id": result.order_id,
            "status": result.status,
            "fill_price": result.fill_price,
            "qty": result.filled_qty,
            "commission": result.commission,
        }
