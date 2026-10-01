# Day 80 – Profiling & Performance Reflection

**Date:** 2026-10-01 · **Level:** Advanced · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_80_profiling_performance/main.py`](../../src/day_80_profiling_performance/main.py) · **Tests:** [`tests/test_day_80.py`](../../tests/test_day_80.py) (8 tests)

## Scenario
An *e-commerce nightly report* that got slow as the shop grew. We measure first (``cProfile``, ``timeit``, ``tracemalloc``/``memory_profiler``), find the hotspots, then apply targeted optimisation patterns – and prove the fast version returns exactly the same answer.

## Syllabus deliverables
> cProfile, timeit, memory\_profiler, and optimization patterns

| Deliverable | Implemented in |
|---|---|
| ✅ cProfile + pstats hotspots | `profile_hotspots` |
| ✅ timeit comparisons | `compare_timings` |
| ✅ memory\_profiler | `memory_profile` |
| ✅ tracemalloc | `peak_allocation_kib` |
| ✅ pattern: set membership instead of list | `report_fast` |
| ✅ pattern: str.join instead of += | `render_csv_fast` |
| ✅ pattern: cache repeated work | `tax_rate` |
| ✅ pattern: generators for streaming | `order_totals` |

## Key learnings
- Measure before optimising: `cProfile` shows which functions consume the time.
- `timeit.repeat` with the minimum gives a stable comparison of alternatives.
- The biggest wins come from algorithms and data structures (set/Counter instead of list scans), not micro-tweaks.

## Pitfalls I hit (and how I fixed them)
- An optimisation is only valid if it returns the same result – every fast path is checked against the slow one.

## Run it
```bash
python -m src.day_80_profiling_performance.main
pytest tests/test_day_80.py -v
```

## Next step
- Tackle advanced regular expressions on Day 81.
