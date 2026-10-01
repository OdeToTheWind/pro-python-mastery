# Day 04 – Variable Naming Rules Reflection

**Date:** 2026-03-16 · **Level:** Beginner · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_04_variable_name_rules/main.py`](../../src/day_04_variable_name_rules/main.py) · **Tests:** [`tests/test_day_04.py`](../../tests/test_day_04.py) (13 tests)

## Scenario
A *code-review bot* that inspects proposed variable names and gives the author syntax errors (must fix) and PEP 8 style warnings (should fix).

## Syllabus deliverables
> PEP 8 naming conventions, reserved keywords, descriptive names and constants

| Deliverable | Implemented in |
|---|---|
| ✅ identifier syntax rules | `review_name` |
| ✅ reserved (hard) keywords | `review_name` |
| ✅ soft keywords (match, case, type, \_) | `review_name` |
| ✅ PEP 8 style classification | `classify_style` |
| ✅ descriptive names | `review_name` |
| ✅ constants | `MAX_LOGIN_ATTEMPTS` |
| ✅ camelCase → snake\_case refactor | `to_snake_case` |

## Key learnings
- `str.isidentifier()` implements the real lexer rules; hand-rolled `isalnum()` checks accept `x²`.
- Hard keywords are errors, soft keywords (`match`, `case`, `type`) are legal but confusing, built-ins can be shadowed.
- Style depends on what the name is for: snake_case variables, CONSTANT_CASE constants, CapWords classes.

## Pitfalls I hit (and how I fixed them)
- Lower-casing every suggestion wrongly told people to rename constants – suggestions are now kind-aware.

## Run it
```bash
python -m src.day_04_variable_name_rules.main
pytest tests/test_day_04.py -v
```

## Next step
- Run `ruff` with the `N` (pep8-naming) rules to enforce this automatically.
