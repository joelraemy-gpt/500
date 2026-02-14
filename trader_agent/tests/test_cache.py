from trader_agent.data.caching import TTLCache


def test_ttl_cache_returns_cached_value() -> None:
    c = TTLCache(ttl_seconds=60)
    calls = {"n": 0}

    def f() -> object:
        calls["n"] += 1
        return calls["n"]

    a = c.get_or_set("x", f)
    b = c.get_or_set("x", f)
    assert a == b == 1
    assert calls["n"] == 1
