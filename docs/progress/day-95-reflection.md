# Day 95 – Performance-critical Module Reflection

**Date:** 2026-10-01 · **Level:** Capstone · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_95_performance_critical_module/main.py`](../../src/day_95_performance_critical_module/main.py) · **Tests:** [`tests/test_day_95.py`](../../tests/test_day_95.py) (9 tests)

## Scenario
A *ride-hailing dispatcher* must find the nearest free driver for every waiting rider, city-wide, several times per second. The same haversine matching is implemented four ways – naive Python, tuned Python with a spatial grid index, vectorised NumPy and (optionally) Numba – then profiled, benchmarked and cross-checked so every fast path returns exactly what the slow, obviously-correct version returns.

## Syllabus deliverables
> Profiling, optimization, and optional Cython/Numba

| Deliverable | Implemented in |
|---|---|
| ✅ baseline (obviously correct) | `nearest_naive` |
| ✅ profiling the baseline | `profile_hotspots` |
| ✅ pure-Python optimisation with a grid index | `nearest_grid` |
| ✅ NumPy vectorisation | `nearest_numpy` |
| ✅ optional Numba JIT with fallback | `nearest_numba` |
| ✅ benchmark harness | `benchmark` |

## Key learnings
- Profile the obvious implementation first; it also serves as the reference for correctness.
- A spatial grid index avoids comparing every rider with every driver.
- NumPy broadcasting computes whole distance matrices at once; Numba is an optional extra.

## Pitfalls I hit (and how I fixed them)
- Every fast path must be checked against the baseline, including ties and sparse, far-away data.

## Run it
```bash
./propython.sh 95                 # study mode: explanation, code map, notes and tests
python -m src.day_95_performance_critical_module.main
pytest tests/test_day_95.py -v
```

## Next step
- Package and release a real tool on Day 96.
