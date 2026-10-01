# Day 79 – Packaging & Distribution Reflection

**Date:** 2026-10-01 · **Level:** Advanced · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_79_packaging_distribution/main.py`](../../src/day_79_packaging_distribution/main.py) · **Tests:** [`tests/test_day_79.py`](../../tests/test_day_79.py) (7 tests)

## Scenario
Publish *"kitchenconv"*, a tiny cooking-unit converter with a CLI, as a real Python package: generate a ``src``-layout project with a complete ``pyproject.toml``, build a wheel and an sdist offline, inspect what is inside, validate the metadata with ``twine check`` and prepare (not perform) the TestPyPI upload.

## Syllabus deliverables
> pyproject.toml, setuptools/hatch/poetry, wheels, and test publishing to PyPI

| Deliverable | Implemented in |
|---|---|
| ✅ pyproject.toml generation | `render_pyproject` |
| ✅ pyproject.toml validation | `validate_pyproject` |
| ✅ build backends compared | `BACKENDS` |
| ✅ src-layout project scaffold | `scaffold` |
| ✅ building wheel + sdist | `build_distributions` |
| ✅ inspecting a wheel | `inspect_wheel` |
| ✅ twine check | `twine_check` |
| ✅ TestPyPI publishing steps | `publish_commands` |

## Key learnings
- `pyproject.toml` holds PEP 621 metadata; the build backend (hatchling, setuptools, poetry-core) is just a pluggable implementation.
- A wheel is a zip of code plus `*.dist-info` metadata; `py3-none-any` means one wheel for every platform.
- `twine check` and a TestPyPI upload rehearse a release safely; tokens belong in environment variables or CI secrets.

## Pitfalls I hit (and how I fixed them)
- `python -m build` normally downloads the backend; `--no-isolation` uses the installed one so builds work offline in CI.

## Run it
```bash
./propython.sh 79                 # study mode: explanation, code map, notes and tests
python -m src.day_79_packaging_distribution.main
pytest tests/test_day_79.py -v
```

## Next step
- Measure and optimise the package's performance on Day 80.
