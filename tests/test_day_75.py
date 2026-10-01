"""Tests for Day 75 – Asyncio Fundamentals (plain asyncio.run, no plugins needed)."""

import asyncio
import inspect
import time

import pytest

from src.day_75_asyncio_fundamentals.main import (
    LATENCY,
    AirlineUnavailable,
    board_sequential,
    board_tolerant,
    board_with_gather,
    board_with_taskgroup,
    fetch_status,
    first_arrivals,
    loop_facts,
    main,
    refresh_in_background,
    status_with_timeout,
)

AIRLINES = list(LATENCY)


def test_coroutine_function():
    assert inspect.iscoroutinefunction(fetch_status)
    flight = asyncio.run(fetch_status("BA"))
    assert (flight.code, flight.status) == ("BA102", "boarding")


def test_gather_runs_concurrently_and_keeps_order():
    start = time.perf_counter()
    flights = asyncio.run(board_with_gather(AIRLINES))
    elapsed = time.perf_counter() - start
    assert [f.code[:2] for f in flights] == AIRLINES
    assert elapsed < sum(LATENCY.values()) * 0.8  # roughly the slowest, not the sum


def test_sequential_takes_the_sum():
    start = time.perf_counter()
    asyncio.run(board_sequential(AIRLINES))
    assert time.perf_counter() - start >= sum(LATENCY.values()) * 0.9


def test_gather_without_return_exceptions_propagates():
    with pytest.raises(AirlineUnavailable):
        asyncio.run(board_with_gather(["LH", "XX"]))


def test_gather_with_return_exceptions():
    assert asyncio.run(board_tolerant(["LH", "XX"])) == {"LH": "on time", "XX": "error: XX service is down"}


def test_taskgroup_success_and_failure():
    assert len(asyncio.run(board_with_taskgroup(["LH", "BA"]))) == 2
    with pytest.raises(ExceptionGroup) as info:
        asyncio.run(board_with_taskgroup(["LH", "XX"]))
    assert isinstance(info.value.exceptions[0], AirlineUnavailable)


def test_as_completed_order_is_by_speed():
    assert asyncio.run(first_arrivals(AIRLINES)) == sorted(AIRLINES, key=LATENCY.__getitem__)


def test_timeout():
    assert asyncio.run(status_with_timeout("AI", 0.01)) == "unknown (timed out)"
    assert asyncio.run(status_with_timeout("BA", 1)) == "boarding"


def test_create_task_and_cancel():
    refreshes, cancelled = asyncio.run(refresh_in_background(3, interval=0.01))
    assert cancelled is True
    assert 2 <= refreshes <= 4


def test_event_loop_facts():
    facts = asyncio.run(loop_facts())
    assert facts["running"] is True
    assert facts["callbacks"] == ["call_soon", "call_later"]
    assert facts["coroutine_is_lazy"] is True


def test_main(capsys):
    main()
    assert "arrival order: ['BA', 'LH', 'EK', 'AI']" in capsys.readouterr().out
