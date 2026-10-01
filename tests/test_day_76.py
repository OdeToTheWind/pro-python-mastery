"""Tests for Day 76 – Advanced Asyncio (a real aiohttp server on localhost, no internet)."""

import asyncio
from decimal import Decimal

import pytest

from src.day_76_advanced_asyncio.main import (
    DEMO_PRICES,
    Offer,
    PriceFeed,
    ShopClient,
    cheapest,
    compare_prices,
    main,
    stream_prices,
    timed_section,
    with_demo_server,
)

SHOPS = list(DEMO_PRICES)


def run(work, **app_kwargs):
    return asyncio.run(with_demo_server(DEMO_PRICES, work, **app_kwargs))


def test_compare_prices_concurrently_with_limit():
    result = run(lambda url: compare_prices(url, SHOPS + ["ghost"], "sku", max_concurrency=2))
    prices = {o.shop: o.price for o in result["offers"]}
    assert prices["pagesplus"] == Decimal("35.50") and prices["ghost"] is None
    assert result["best"].shop == "pagesplus"
    assert result["max_in_flight"] == 2
    assert result["log"][0].startswith("compare: ")


def test_concurrency_is_faster_than_sequential():
    result = run(lambda url: compare_prices(url, SHOPS, "sku", max_concurrency=4), delay=0.1)
    seconds = float(result["log"][0].split(": ")[1].rstrip("s"))
    assert seconds < 0.3  # four 0.1 s requests overlap


def test_retry_recovers_from_transient_503():
    async def work(url):
        async with ShopClient(url, retries=1) as client:
            return await client.fetch_price("readmore", "sku")

    assert run(work, flaky={"readmore"}).price == Decimal("41.00")


def test_errors_become_offers_not_crashes():
    async def work(url):
        async with ShopClient(url, retries=0) as client:
            return await client.fetch_price("readmore", "sku")

    offer = run(work, flaky={"readmore"})
    assert offer.price is None and offer.error == "ClientResponseError"


def test_timeout_is_reported():
    async def work(url):
        async with ShopClient(url, timeout=0.05, retries=0) as client:
            return await client.fetch_price("inkwell", "sku")

    assert run(work, delay=0.5).error == "TimeoutError"


def test_client_requires_async_with():
    with pytest.raises(RuntimeError, match="async with"):
        asyncio.run(ShopClient("http://x").fetch_price("a", "b"))


def test_session_closed_on_exit():
    async def work(url):
        async with ShopClient(url) as client:
            session = client._session
        return session.closed

    assert run(work) is True


def test_async_iterator_class():
    async def work(url):
        async with ShopClient(url) as client:
            return [offer.shop async for offer in PriceFeed(client, ["inkwell", "bookhaven"], "sku")]

    assert run(work) == ["inkwell", "bookhaven"]


def test_async_generator_streams_and_cheapest():
    async def work(url):
        async with ShopClient(url) as client:
            return await cheapest(stream_prices(client, SHOPS + ["ghost"], "sku"))

    assert run(work) == Offer("pagesplus", Decimal("35.50"))


def test_cheapest_of_nothing():
    async def empty():
        return
        yield

    assert asyncio.run(cheapest(empty())) is None


def test_asynccontextmanager_logs_even_on_error():
    log = []
    ticks = iter([1.0, 3.5])

    async def work():
        async with timed_section("x", log, clock=lambda: next(ticks)):
            raise ValueError

    with pytest.raises(ValueError):
        asyncio.run(work())
    assert log == ["x: 2.500s"]


def test_main(capsys):
    main()
    out = capsys.readouterr().out
    assert "readmore    41.00" in out and "closedshop  ClientResponseError" in out
