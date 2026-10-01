# Day 81 – Advanced Regular Expressions Reflection

**Date:** 2026-10-01 · **Level:** Advanced · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_81_advanced_regular_expressions/main.py`](../../src/day_81_advanced_regular_expressions/main.py) · **Tests:** [`tests/test_day_81.py`](../../tests/test_day_81.py) (11 tests)

## Scenario
A *customer-support ticket parser* that pulls order numbers, amounts, dates and contact details out of free-text emails, redacts personal data before it reaches the logs, and normalises messy formatting.

## Syllabus deliverables
> Complex patterns, groups, lookarounds, and the re module

| Deliverable | Implemented in |
|---|---|
| ✅ verbose pattern with comments | `ORDER_RE` |
| ✅ named groups + groupdict | `parse_amounts` |
| ✅ non-capturing groups and alternation | `DATE_RE` |
| ✅ backreferences | `find_repeated_words` |
| ✅ lookahead / negative lookahead | `is_strong_reference` |
| ✅ lookbehind | `parse_amounts` |
| ✅ sub with a replacement function | `redact` |
| ✅ split on a pattern | `split_sentences` |
| ✅ fullmatch for validation | `valid_order_number` |
| ✅ safe vs catastrophic patterns | `SAFE_EMAIL_RE` |

## Key learnings
- Verbose patterns (`re.VERBOSE`) with named groups make complex regexes readable and reviewable.
- Lookarounds check context (a currency sign before, a digit after) without consuming characters.
- `re.sub` with a function can transform each match – e.g. redact while keeping triage hints.

## Pitfalls I hit (and how I fixed them)
- Greedy quantifiers and unanchored patterns match far more than intended; `fullmatch` and tests with near-misses catch this.

## Run it
```bash
./propython.sh 81                 # study mode: explanation, code map, notes and tests
python -m src.day_81_advanced_regular_expressions.main
pytest tests/test_day_81.py -v
```

## Next step
- Store structured data properly in SQLite on Day 82.
