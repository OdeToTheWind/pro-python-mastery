# Day 73 – Concurrency: Threading Reflection

**Date:** 2026-10-01 · **Level:** Advanced · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_73_concurrency_threading/main.py`](../../src/day_73_concurrency_threading/main.py) · **Tests:** [`tests/test_day_73.py`](../../tests/test_day_73.py) (9 tests)

## Scenario
A *photo-sharing upload service*. Thumbnails are fetched from slow storage (I/O bound → threads help), view counters are updated from many threads (needs a lock), and uploads flow through a producer/consumer queue. A CPU-bound resize shows why the GIL limits threads for pure-Python work.

## Syllabus deliverables
> threading, locks, queues, and GIL implications

| Deliverable | Implemented in |
|---|---|
| ✅ threading.Thread | `upload_pipeline` |
| ✅ ThreadPoolExecutor | `fetch_thumbnails` |
| ✅ race condition | `ViewCounter.unsafe_increment` |
| ✅ Lock | `ViewCounter.safe_increment` |
| ✅ queue.Queue producer/consumer | `upload_pipeline` |
| ✅ threading.Event for shutdown | `Heartbeat` |
| ✅ GIL implications: I/O vs CPU | `gil_experiment` |

## Key learnings
- Threads help with I/O-bound work: while one waits on the network, others run.
- Read-modify-write on shared state is a race; a `Lock` makes the section atomic.
- `queue.Queue` is the safe hand-over point between producers and consumers; sentinels stop workers cleanly.

## Pitfalls I hit (and how I fixed them)
- With the GIL, pure-Python CPU work does not get faster with threads – the experiment shows a speed-up near 1×.

## Run it
```bash
python -m src.day_73_concurrency_threading.main
pytest tests/test_day_73.py -v
```

## Next step
- Use separate processes for CPU-bound work on Day 74.
