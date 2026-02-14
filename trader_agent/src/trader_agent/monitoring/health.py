from __future__ import annotations


def health_report(feed_ok: bool, broker_ok: bool, latency_ms: float) -> dict:
    return {
        "feed_ok": feed_ok,
        "broker_ok": broker_ok,
        "latency_ms": latency_ms,
        "status": "ok" if feed_ok and broker_ok and latency_ms < 2_000 else "degraded",
    }
