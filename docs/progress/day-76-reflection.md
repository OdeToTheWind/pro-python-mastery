# Day 76 – Advanced Asyncio Reflection

**Date:** 2026-10-01 · **Level:** Advanced · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_76_advanced_asyncio/main.py`](../../src/day_76_advanced_asyncio/main.py) · **Tests:** [`tests/test_day_76.py`](../../tests/test_day_76.py) (12 tests)

## Scenario
A *price-comparison engine* that asks many online shops for the price of a product concurrently with ``aiohttp`` – politely (connection limits), safely (timeouts, retries) and streaming results as they arrive.

## Syllabus deliverables
> Async context managers, async iterators, and concurrent HTTP with aiohttp

| Deliverable | Implemented in |
|---|---|
| ✅ async context manager class | `ShopClient` |
| ✅ @asynccontextmanager | `timed_section` |
| ✅ async iterator class (\_\_aiter\_\_/\_\_anext\_\_) | `PriceFeed` |
| ✅ async generator | `stream_prices` |
| ✅ concurrent HTTP with aiohttp | `compare_prices` |
| ✅ limiting concurrency with a Semaphore | `ShopClient.fetch_price` |
| ✅ timeouts and retries | `ShopClient.fetch_price` |
| ✅ async comprehension | `cheapest` |

## Key learnings
- Reuse one `aiohttp.ClientSession` per client – it owns the connection pool and must be closed in `__aexit__`.
- A `Semaphore` caps requests in flight so concurrency stays polite to servers.
- Async generators stream results as they finish; cancel outstanding tasks if the consumer stops early.

## Pitfalls I hit (and how I fixed them)
- Tests must never depend on the internet – a local aiohttp `TestServer` makes the HTTP lesson real and deterministic.

## Run it
```bash
python -m src.day_76_advanced_asyncio.main
pytest tests/test_day_76.py -v
```

## Next step
- Log what the client does with structured logging on Day 77.
