# Day 29 – Using External Python Modules / Import Reflection

**Date:** 2026-04-10 · **Level:** Intermediate · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_29_external_modules/main.py`](../../src/day_29_external_modules/main.py) · **Tests:** [`tests/test_day_29.py`](../../tests/test_day_29.py) (10 tests)

## Scenario
A *dependency inspector* for this course – it checks which third-party packages are installed, reads their versions, uses one of them (``requests``) offline, and organises its own helpers as a local package.

## Syllabus deliverables
> import statements, package installation, and module organization

| Deliverable | Implemented in |
|---|---|
| ✅ import statements (absolute, relative, from-import) | `toolkit` |
| ✅ lazy / optional imports | `optional_import` |
| ✅ checking installed packages | `is_installed` |
| ✅ reading package versions | `installed_version` |
| ✅ verifying requirements | `check_requirement` |
| ✅ using a third-party library | `build_query_url` |
| ✅ module organisation (package + \_\_all\_\_) | `toolkit` |

## Key learnings
- `importlib.util.find_spec` checks for a module without importing it; `importlib.metadata.version` reads installed versions.
- A package's `__init__.py` and `__all__` define its public API.
- Optional imports keep features working when an extra dependency is absent.

## Pitfalls I hit (and how I fixed them)
- Third-party dependencies must be listed in `requirements.txt` – `packaging` was implicit before.

## Run it
```bash
./propython.sh 29                 # study mode: explanation, code map, notes and tests
python -m src.day_29_external_modules.main
pytest tests/test_day_29.py -v
```

## Next step
- Turn the toolkit into an installable package on Day 79.
