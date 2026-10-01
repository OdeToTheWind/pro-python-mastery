# Day 85 – Concurrent File / Network Processor Reflection

**Date:** 2026-10-01 · **Level:** Capstone · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_85_concurrent_file_network_processor/main.py`](../../src/day_85_concurrent_file_network_processor/main.py) · **Tests:** [`tests/test_day_85.py`](../../tests/test_day_85.py) (11 tests)

## Scenario
A *podcast-archive mirroring tool*. Episodes are downloaded from a feed server with asyncio (I/O bound, hundreds of sockets on one thread), verified with SHA-256 in a thread pool (disk I/O releases the GIL), and compressed for cold storage in a process pool (pure CPU work). One report tells the operator what succeeded, what failed and why.

## Syllabus deliverables
> Thread/process pools or asyncio for I/O-bound work

| Deliverable | Implemented in |
|---|---|
| ✅ asyncio downloads with a concurrency limit | `download_all` |
| ✅ retries and timeouts per request | `download_one` |
| ✅ thread pool for file hashing | `checksum_files` |
| ✅ process pool for compression | `compress_files` |
| ✅ thread-safe progress counter | `Progress` |
| ✅ strategy per workload | `choose_executor` |
| ✅ end-to-end mirror run | `mirror` |

## Key learnings
- asyncio suits many network waits, threads suit blocking file I/O, and processes suit CPU-bound work.
- A semaphore caps concurrent requests; retries with backoff absorb transient 5xx errors.
- `as_completed` handles results as soon as each finishes and collects failures without stopping the run.

## Pitfalls I hit (and how I fixed them)
- Forking a multi-threaded process can deadlock – the `spawn` start method is the safe, portable choice.

## Run it
```bash
python -m src.day_85_concurrent_file_network_processor.main
pytest tests/test_day_85.py -v
```

## Next step
- Build structured logging and metrics on Day 86.
