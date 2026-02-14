from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from trader_agent.storage.models import Base, DecisionEvent, ErrorEvent, OrderEvent, SignalEvent


class Storage:
    def __init__(self, db_url: str) -> None:
        self.engine = create_engine(db_url, future=True)
        self.Session = sessionmaker(bind=self.engine, class_=Session, expire_on_commit=False)

    def init(self) -> None:
        Base.metadata.create_all(self.engine)

    def add_signal(self, symbol: str, direction: str, confidence: float, rationale: str) -> None:
        with self.Session() as s:
            s.add(SignalEvent(symbol=symbol, direction=direction, confidence=confidence, rationale=rationale, created_at=datetime.now(tz=timezone.utc)))
            s.commit()

    def add_decision(self, allowed: bool, reason: str) -> None:
        with self.Session() as s:
            s.add(DecisionEvent(allowed=str(allowed), reason=reason, created_at=datetime.now(tz=timezone.utc)))
            s.commit()

    def add_order(self, order_id: str, symbol: str, side: str, qty: float, fill_price: float, status: str) -> None:
        with self.Session() as s:
            s.add(OrderEvent(order_id=order_id, symbol=symbol, side=side, qty=qty, fill_price=fill_price, status=status, created_at=datetime.now(tz=timezone.utc)))
            s.commit()

    def add_error(self, error_type: str, message: str) -> None:
        with self.Session() as s:
            s.add(ErrorEvent(error_type=error_type, message=message, created_at=datetime.now(tz=timezone.utc)))
            s.commit()
