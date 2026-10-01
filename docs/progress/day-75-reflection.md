# Day 75 – Asyncio Fundamentals Reflection

**Date:** 2026-10-01 · **Level:** Advanced · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_75_asyncio_fundamentals/main.py`](../../src/day_75_asyncio_fundamentals/main.py) · **Tests:** [`tests/test_day_75.py`](../../tests/test_day_75.py) (11 tests)

## Scenario
An *airport departures board* that queries several airline status services at once. Each query mostly waits on the network, so one thread with an event loop can overlap all of them.

## Syllabus deliverables
> Event loop, coroutines, async/await, gather, and create\_task

| Deliverable | Implemented in |
|---|---|
| ✅ coroutine function (async def) | `fetch_status` |
| ✅ await | `fetch_status` |
| ✅ event loop (asyncio.run / get\_running\_loop) | `loop_facts` |
| ✅ gather | `board_with_gather` |
| ✅ gather with return\_exceptions | `board_tolerant` |
| ✅ create\_task and cancellation | `refresh_in_background` |
| ✅ TaskGroup (structured concurrency) | `board_with_taskgroup` |
| ✅ as\_completed | `first_arrivals` |
| ✅ timeouts | `status_with_timeout` |

## Key learnings
- A coroutine does nothing until awaited; the event loop switches between coroutines at each `await`.
- `gather` runs awaitables concurrently and keeps result order; `return_exceptions=True` keeps one failure from losing the others.
- `create_task` starts background work immediately; `TaskGroup` gives structured concurrency with automatic cancellation.

## Pitfalls I hit (and how I fixed them)
- A cancelled task must still be awaited, otherwise the cancellation is never processed – `contextlib.suppress(CancelledError)` keeps it tidy.

## Run it
```bash
python -m src.day_75_asyncio_fundamentals.main
pytest tests/test_day_75.py -v
```

## Next step
- Add async context managers, async iterators and real HTTP on Day 76.
