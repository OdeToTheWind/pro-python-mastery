# Day 23 – Scope and Local/Global Variables Reflection

**Date:** 2026-04-04 · **Level:** Beginner · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_23_scope_local_global_variables/main.py`](../../src/day_23_scope_local_global_variables/main.py) · **Tests:** [`tests/test_day_23.py`](../../tests/test_day_23.py) (7 tests)

## Scenario
A *web-app feature-flag service*. Configuration lives at module level, request handlers have their own locals and rate limiters are closures.

## Syllabus deliverables
> LEGB rule, global and nonlocal usage, and good scoping practices

| Deliverable | Implemented in |
|---|---|
| ✅ LEGB lookup order | `legb_trace` |
| ✅ global keyword | `set_environment` |
| ✅ nonlocal keyword | `make_rate_limiter` |
| ✅ UnboundLocalError pitfall | `unbound_local_demo` |
| ✅ closures and captured cells | `closure_cells` |
| ✅ good practice: explicit state instead of globals | `FeatureFlags` |

## Key learnings
- LEGB: Local → Enclosing → Global → Built-in, and the first match wins.
- Assigning anywhere in a function makes the name local everywhere in it (`UnboundLocalError`).
- Closures store captured variables in cells you can inspect via `__closure__`.

## Pitfalls I hit (and how I fixed them)
- The original demo labelled a local of `main()` as 'global' – a real module global is now used.

## Run it
```bash
python -m src.day_23_scope_local_global_variables.main
pytest tests/test_day_23.py -v
```

## Next step
- Prefer explicit objects (`FeatureFlags`) over module globals in larger programs.
