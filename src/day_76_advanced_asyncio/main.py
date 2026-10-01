"""Day 76 – Advanced Asyncio.

Scenario: a *price-comparison engine* that asks many online shops for the
price of a product concurrently with ``aiohttp`` – politely (connection limits),
safely (timeouts, retries) and streaming results as they arrive.

Deliverables (syllabus):
* Async context managers (``__aenter__``/``__aexit__`` and ``@asynccontextmanager``)
* Async iterators (``__aiter__``/``__anext__`` and async generators)
* Concurrent HTTP with ``aiohttp`` (one session, semaphore, timeouts, retries)
"""

from __future__ import annotations

import asyncio
import contextlib
from collections.abc import AsyncIterator, Awaitable, Callable
from dataclasses import dataclass
from decimal import Decimal
from types import TracebackType
from typing import Self

import aiohttp

DELIVERABLES: dict[str, str] = {
    "async context manager class": "ShopClient",
    "@asynccontextmanager": "timed_section",
    "async iterator class (__aiter__/__anext__)": "PriceFeed",
    "async generator": "stream_prices",
    "concurrent HTTP with aiohttp": "compare_prices",
    "limiting concurrency with a Semaphore": "ShopClient.fetch_price",
    "timeouts and retries": "ShopClient.fetch_price",
    "async comprehension": "cheapest",
}


@dataclass(frozen=True, slots=True)
class Offer:
    shop: str
    price: Decimal | None
    error: str | None = None


class ShopClient:
    """Owns one ``aiohttp.ClientSession`` (connection pool) for its lifetime."""

    def __init__(self, base_url: str, *, max_concurrency: int = 3, timeout: float = 2.0,
                 retries: int = 1) -> None:
        self.base_url = base_url.rstrip("/")
        self.semaphore = asyncio.Semaphore(max_concurrency)
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.retries = retries
        self.in_flight = 0
        self.max_in_flight = 0
        self._session: aiohttp.ClientSession | None = None

    async def __aenter__(self) -> Self:
        self._session = aiohttp.ClientSession(timeout=self.timeout,
                                              headers={"User-Agent": "ProPythonMastery-Day76"})
        return self

    async def __aexit__(self, exc_type: type[BaseException] | None, exc: BaseException | None,
                        tb: TracebackType | None) -> None:
        if self._session is not None:
            await self._session.close()  # always release sockets, even on errors

    async def fetch_price(self, shop: str, sku: str) -> Offer:
        if self._session is None:
            raise RuntimeError("use 'async with ShopClient(...)'")
        url = f"{self.base_url}/{shop}/price/{sku}"
        for attempt in range(self.retries + 1):
            async with self.semaphore:  # at most N requests in flight
                self.in_flight += 1
                self.max_in_flight = max(self.max_in_flight, self.in_flight)
                try:
                    async with self._session.get(url) as response:
                        if response.status == 503 and attempt < self.retries:
                            continue  # transient – try again
                        response.raise_for_status()
                        data = await response.json()
                        return Offer(shop, Decimal(str(data["price"])))
                except (aiohttp.ClientError, TimeoutError, KeyError) as exc:
                    if attempt == self.retries:
                        return Offer(shop, None, f"{type(exc).__name__}")
                finally:
                    self.in_flight -= 1
        return Offer(shop, None, "unavailable")


class PriceFeed:
    """A hand-written async iterator: one request per ``__anext__``."""

    def __init__(self, client: ShopClient, shops: list[str], sku: str) -> None:
        self.client, self.shops, self.sku = client, list(shops), sku

    def __aiter__(self) -> Self:
        return self

    async def __anext__(self) -> Offer:
        if not self.shops:
            raise StopAsyncIteration
        return await self.client.fetch_price(self.shops.pop(0), self.sku)


async def stream_prices(client: ShopClient, shops: list[str], sku: str) -> AsyncIterator[Offer]:
    """An async generator yielding offers *as they arrive* (all requests run concurrently)."""
    tasks = [asyncio.create_task(client.fetch_price(shop, sku)) for shop in shops]
    try:
        for finished in asyncio.as_completed(tasks):
            yield await finished
    finally:
        for task in tasks:
            task.cancel()  # if the consumer stops early, don't leave requests running


async def cheapest(offers: AsyncIterator[Offer]) -> Offer | None:
    """Async comprehension collects from an async iterator."""
    valid = [offer async for offer in offers if offer.price is not None]
    return min(valid, key=lambda o: o.price or Decimal("0"), default=None)


@contextlib.asynccontextmanager
async def timed_section(label: str, log: list[str],
                        clock: Callable[[], float] | None = None) -> AsyncIterator[None]:
    loop_time = clock or asyncio.get_running_loop().time
    start = loop_time()
    try:
        yield
    finally:
        log.append(f"{label}: {loop_time() - start:.3f}s")


async def compare_prices(base_url: str, shops: list[str], sku: str, *, max_concurrency: int = 3) -> dict[str, object]:
    log: list[str] = []
    async with ShopClient(base_url, max_concurrency=max_concurrency) as client, timed_section("compare", log):
        offers = await asyncio.gather(*(client.fetch_price(shop, sku) for shop in shops))
        best = min((o for o in offers if o.price is not None), key=lambda o: o.price or 0, default=None)
    return {"offers": offers, "best": best, "max_in_flight": client.max_in_flight, "log": log}


# ----- a tiny local shop server so the demo and tests never need the internet -----

def build_demo_app(prices: dict[str, Decimal], delay: float = 0.05, flaky: set[str] | None = None) -> aiohttp.web.Application:
    from aiohttp import web

    failures: dict[str, int] = {}

    async def price(request: web.Request) -> web.Response:
        shop = request.match_info["shop"]
        await asyncio.sleep(delay)
        if flaky and shop in flaky and failures.get(shop, 0) == 0:
            failures[shop] = 1
            return web.Response(status=503)
        if shop not in prices:
            return web.Response(status=404)
        return web.json_response({"shop": shop, "sku": request.match_info["sku"], "price": str(prices[shop])})

    app = web.Application()
    app.router.add_get("/{shop}/price/{sku}", price)
    return app


async def with_demo_server(prices: dict[str, Decimal], work: Callable[[str], Awaitable[object]],
                           **app_kwargs: object) -> object:
    from aiohttp.test_utils import TestServer

    server = TestServer(build_demo_app(prices, **app_kwargs))  # type: ignore[arg-type]
    await server.start_server()
    try:
        return await work(str(server.make_url("")))
    finally:
        await server.close()


DEMO_PRICES = {"bookhaven": Decimal("39.90"), "pagesplus": Decimal("35.50"),
               "readmore": Decimal("41.00"), "inkwell": Decimal("36.10")}


def main() -> None:
    print("Day 76 – Price comparison (local demo shops)\n")
    shops = [*DEMO_PRICES, "closedshop"]
    result = asyncio.run(with_demo_server(DEMO_PRICES, lambda url: compare_prices(url, shops, "978-1492056355"),
                                          flaky={"readmore"}))
    assert isinstance(result, dict)
    for offer in result["offers"]:
        print(f"  {offer.shop:<11} {offer.price or offer.error}")
    print("best:", result["best"], "| max in flight:", result["max_in_flight"], "|", result["log"])


if __name__ == "__main__":
    main()
