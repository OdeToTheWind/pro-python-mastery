# Day 92 – Test Suite for a Multi-module Package Reflection

**Date:** 2026-10-01 · **Level:** Capstone · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_92_multi_module_test_suite/main.py`](../../src/day_92_multi_module_test_suite/main.py) · **Tests:** [`tests/test_day_92.py`](../../tests/test_day_92.py) (13 tests)

## Scenario
``lending`` – a *community library lending system* split into ``models``, ``repository``, ``notifier`` and ``service`` modules. The point of the day is the **test suite**: factory fixtures, a fake repository, mocked notifications, a frozen clock, parametrised business rules and a CI command that enforces >90 % branch coverage for the package.

## Syllabus deliverables
> High coverage, fixtures, mocks, and CI-friendly structure

| Deliverable | Implemented in |
|---|---|
| ✅ models module (rules on single objects) | `models.Loan.fine` |
| ✅ repository module (Protocol + JSON storage) | `repository.JsonRepository` |
| ✅ notifier module (mockable side effects) | `notifier.Notifier` |
| ✅ service module (injected dependencies) | `service.LendingService` |
| ✅ CI command with coverage gate | `CI_COMMAND` |

## Key learnings
- Injecting dependencies (repository, notifier, clock) is what makes a package easy to test.
- Factory fixtures, fakes and `create_autospec` mocks test behaviour without real e-mail or disk.
- One deterministic CI command with a branch-coverage gate keeps quality from slipping.

## Pitfalls I hit (and how I fixed them)
- Plain `Mock()` accepts any call; `create_autospec` fails when the real signature changes.

## Run it
```bash
./propython.sh 92                 # study mode: explanation, code map, notes and tests
python -m src.day_92_multi_module_test_suite.main
pytest tests/test_day_92.py -v
```

## Next step
- Write an asyncio network service on Day 93.
