from trader_agent.strategy.examples import MovingAverageCrossoverStrategy


def test_strategy_determinism_on_bar() -> None:
    s1 = MovingAverageCrossoverStrategy(short_window=2, long_window=3)
    s2 = MovingAverageCrossoverStrategy(short_window=2, long_window=3)
    prices = [100.0, 101.0, 102.0, 103.0]
    out1 = [s1.on_bar("AAPL", p) for p in prices]
    out2 = [s2.on_bar("AAPL", p) for p in prices]
    assert [o.direction if o else None for o in out1] == [o.direction if o else None for o in out2]
