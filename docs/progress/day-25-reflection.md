# Day 25 – Local Development Environment Setup Reflection

**Date:** 2026-04-06 · **Level:** Intermediate · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_25_dev_env_setup_local/main.py`](../../src/day_25_dev_env_setup_local/main.py) · **Tests:** [`tests/test_day_25.py`](../../tests/test_day_25.py) (9 tests)

## Scenario
A *project doctor* that inspects a checkout (this repository by default) and reports whether the local environment follows best practice.

## Syllabus deliverables
> Virtual environments, project structure, and local development best practices

| Deliverable | Implemented in |
|---|---|
| ✅ virtual environment detection | `in_virtualenv` |
| ✅ interpreter version check | `python_version_ok` |
| ✅ project structure check | `check_structure` |
| ✅ dependency hygiene | `audit_requirements` |
| ✅ .gitignore best practices | `missing_ignore_rules` |

## Key learnings
- `sys.prefix != sys.base_prefix` detects a venv even when `activate` was never run.
- Duplicate or unpinned requirements make installs non-reproducible.
- `.gitignore` must cover `.venv/`, `__pycache__/` and `.env` from day one.

## Pitfalls I hit (and how I fixed them)
- This repository itself had duplicate `pytest` lines and an ignored-but-missing `.env` rule – the doctor caught both.

## Run it
```bash
./propython.sh 25                 # study mode: explanation, code map, notes and tests
python -m src.day_25_dev_env_setup_local.main
pytest tests/test_day_25.py -v
```

## Next step
- Move to `pyproject.toml` dependency groups when packaging on Day 79.
