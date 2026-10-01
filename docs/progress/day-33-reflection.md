# Day 33 – Module Aliasing Reflection

**Date:** 2026-04-14 · **Level:** Intermediate · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_33_module_aliasing/main.py`](../../src/day_33_module_aliasing/main.py) · **Tests:** [`tests/test_day_33.py`](../../tests/test_day_33.py) (7 tests)

## Scenario
A *fitness-tracker weekly summary* that needs two different ``loads`` functions and some long module names – aliasing keeps it readable.

## Syllabus deliverables
> import module as alias, code organization and readability

| Deliverable | Implemented in |
|---|---|
| ✅ import module as alias | `weekly_summary` |
| ✅ from module import name as alias | `load_settings` |
| ✅ resolving name clashes | `load_settings` |
| ✅ readability guidelines | `ALIAS_GUIDE` |
| ✅ inspecting what an alias refers to | `resolve_aliases` |

## Key learnings
- Conventional aliases (`np`, `pd`, `dt`) aid readability; single-letter custom aliases hurt it.
- `from x import loads as json_loads` resolves real name clashes.
- An alias is just another name bound to the same module object.

## Pitfalls I hit (and how I fixed them)
- `tomllib.loads` actually lives in a private submodule – inspect `__module__` rather than assuming.

## Run it
```bash
python -m src.day_33_module_aliasing.main
pytest tests/test_day_33.py -v
```

## Next step
- Keep imports sorted and aliased consistently with ruff's `I` rules.
