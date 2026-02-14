from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_env: str = "dev"
    log_level: str = "INFO"
    log_json: bool = True
    db_url: str = "sqlite:///trader_agent.db"

    mode: str = "paper"
    live_trading: bool = False
    symbols: str = "AAPL,MSFT"
    interval: str = "1m"
    loop_sleep_seconds: float = 1.0

    risk_per_trade_pct: float = Field(0.5, ge=0.01, le=5)
    max_daily_loss_pct: float = Field(2.0, ge=0.1, le=100)
    max_trades_per_day: int = 10
    max_open_positions: int = 5
    max_exposure_per_symbol_pct: float = 25.0
    max_total_exposure_pct: float = 80.0
    require_stop_loss: bool = True

    circuit_breaker_feed_errors: int = 5

    default_broker: str = "paper"
    paper_initial_equity: float = 100_000.0
    paper_commission_per_trade: float = 1.0
    paper_slippage_bps: float = 2.0

    market_data_provider: str = "mock"
    cache_ttl_seconds: int = 30
    rate_limit_per_min: int = 60

    human_confirmation_required: bool = True


settings = Settings()
