"""Tests for Day 67 – Decorators Deep Dive."""

import inspect

import pytest

from src.day_67_decorators_deep_dive.main import (
    STACKING_ORDER,
    RateLimit,
    describe_latitude,
    forecast,
    main,
    memoize_by,
    naive_timed,
    retry,
    stacked,
    timed,
    validate_range,
)


def sample(city: str, units: str = "metric") -> str:
    """Docstring of sample."""
    return f"{city}/{units}"


def test_wraps_preserves_metadata():
    wrapped = timed(sample)
    assert wrapped.__name__ == "sample"
    assert wrapped.__doc__ == "Docstring of sample."
    assert wrapped.__wrapped__ is sample
    assert str(inspect.signature(wrapped)) == "(city: str, units: str = 'metric') -> str"


def test_without_wraps_metadata_is_lost():
    assert naive_timed(sample).__name__ == "wrapper"
    assert naive_timed(sample).__doc__ is None


def test_timed_records_even_when_function_raises():
    @timed
    def boom():
        raise RuntimeError

    with pytest.raises(RuntimeError):
        boom()
    assert len(boom.timings) == 1 and boom.timings[0] >= 0


def test_retry_succeeds_after_failures():
    calls, waits = [], []

    @retry(times=3, delay=0.5, sleep=waits.append)
    def flaky():
        calls.append(1)
        if len(calls) < 3:
            raise ConnectionError
        return "ok"

    assert flaky() == "ok"
    assert waits == [0.5, 1.0]


def test_retry_gives_up_and_ignores_other_errors():
    @retry(times=2, sleep=lambda _s: None)
    def down():
        raise ConnectionError("down")

    with pytest.raises(ConnectionError):
        down()

    @retry(times=5, sleep=lambda _s: None)
    def bug():
        raise KeyError("not retried")

    with pytest.raises(KeyError):
        bug()
    with pytest.raises(ValueError):
        retry(times=0)


def test_validate_range_with_and_without_arguments():
    assert describe_latitude(10) == "northern"
    with pytest.raises(ValueError, match="describe_latitude: 95"):
        describe_latitude(95)

    @validate_range(low=0, high=100)
    def humidity(value):
        return f"{value}%"

    assert humidity(55) == "55%"
    with pytest.raises(ValueError):
        humidity(-1)


def test_class_based_rate_limit_keeps_state():
    now = [0.0]
    limiter = RateLimit(calls=2, per_seconds=10, clock=lambda: now[0])

    @limiter
    def ping():
        return "pong"

    assert [ping(), ping()] == ["pong", "pong"]
    with pytest.raises(RuntimeError, match="rate limit"):
        ping()
    now[0] = 10.5
    assert ping() == "pong"
    assert ping.limiter is limiter and ping.__name__ == "ping"


def test_memoize_by_custom_key():
    calls = []

    @memoize_by(lambda city: city.lower())
    def lookup(city):
        calls.append(city)
        return len(calls)

    assert lookup("Paris") == lookup("PARIS") == 1
    assert calls == ["Paris"] and lookup.cache == {"paris": 1}


def test_forecast_combines_decorators():
    assert forecast(" oslo ") == "Oslo: 21°C, light breeze"
    assert forecast("OSLO") == "Oslo: 21°C, light breeze"
    assert "oslo" in forecast.cache


def test_stacking_order():
    STACKING_ORDER.clear()
    assert stacked() == "done"
    assert STACKING_ORDER == ["outer", "inner"]


def test_main(capsys):
    main()
    out = capsys.readouterr().out
    assert "retry: ok after 3 attempts" in out and "naive name: wrapper" in out
