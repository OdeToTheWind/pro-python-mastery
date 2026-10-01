# Day 78 – Testing with pytest Reflection

**Date:** 2026-10-01 · **Level:** Advanced · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_78_testing_with_pytest/main.py`](../../src/day_78_testing_with_pytest/main.py) · **Tests:** [`tests/test_day_78.py`](../../tests/test_day_78.py) (14 tests)

## Scenario
A *parcel-shipping quote service* that calls a carrier's rate API. This module is the code under test; ``tests/test_day_78.py`` is the real lesson – it shows fixtures (scopes, factories, teardown, built-ins), parametrisation (ids, stacked parameters), mocking (``Mock(spec=...)``, ``patch``, ``monkeypatch``, call assertions) and coverage.

## Syllabus deliverables
> Fixtures, parametrization, mocking, and coverage

| Deliverable | Implemented in |
|---|---|
| ✅ code under test with an injectable dependency | `QuoteService` |
| ✅ factory used by fixtures | `make_parcel` |
| ✅ fake carrier (test double) | `FakeCarrier` |
| ✅ table used for parametrisation | `ZONE_CASES` |
| ✅ time source to monkeypatch | `QuoteService.quote` |
| ✅ coverage measured programmatically | `measure_coverage` |

## Key learnings
- Fixtures build what a test needs and clean up after `yield`; factory fixtures keep tests short and explicit.
- Stacked `parametrize` decorators multiply cases; `ids` and `pytest.param` make failures readable.
- `Mock(spec=...)` fails on methods the real class doesn't have, and call assertions verify interactions.

## Pitfalls I hit (and how I fixed them)
- `assert a == b if cond else c` parses as `assert (a == b) if cond else c` – one branch silently asserted nothing until rewritten.

## Run it
```bash
python -m src.day_78_testing_with_pytest.main
pytest tests/test_day_78.py -v
```

## Next step
- Package a tested project for distribution on Day 79.
