# Day 74 – Concurrency: Multiprocessing Reflection

**Date:** 2026-10-01 · **Level:** Advanced · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_74_concurrency_multiprocessing/main.py`](../../src/day_74_concurrency_multiprocessing/main.py) · **Tests:** [`tests/test_day_74.py`](../../tests/test_day_74.py) (8 tests)

## Scenario
A *satellite-image analysis lab*. Counting "bright pixels" in large tiles is pure CPU work, so it runs in a process pool (each process has its own interpreter and GIL). Tiles are shared through ``shared_memory`` instead of being copied, and a small advisor decides when processes beat threads.

## Syllabus deliverables
> Process pools, shared memory, and choosing processes vs. threads

| Deliverable | Implemented in |
|---|---|
| ✅ ProcessPoolExecutor | `analyse_tiles` |
| ✅ multiprocessing.Pool with chunksize | `analyse_tiles_pool` |
| ✅ shared\_memory (zero-copy buffers) | `bright_pixels_shared` |
| ✅ shared Value with a lock | `count_with_shared_value` |
| ✅ processes vs threads decision | `choose_executor` |
| ✅ measuring speed-up and overhead | `benchmark` |

## Key learnings
- Each process has its own interpreter and GIL, so CPU-bound work scales across cores.
- Arguments and results are pickled between processes – small tasks can be slower in parallel than sequentially.
- `shared_memory` shares one buffer by name instead of copying it; always `close()` and `unlink()` it.

## Pitfalls I hit (and how I fixed them)
- Forgetting `unlink()` leaks the OS shared-memory block until reboot – a test now proves it is released.

## Run it
```bash
python -m src.day_74_concurrency_multiprocessing.main
pytest tests/test_day_74.py -v
```

## Next step
- Handle thousands of I/O waits in one thread with asyncio on Day 75.
