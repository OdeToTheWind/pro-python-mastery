# Day 64 – Iterators & the Iterator Protocol Reflection

**Date:** 2026-10-01 · **Level:** Advanced · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_64_iterators_iterator_protocol/main.py`](../../src/day_64_iterators_iterator_protocol/main.py) · **Tests:** [`tests/test_day_64.py`](../../tests/test_day_64.py) (11 tests)

## Scenario
A *paginated API cursor for a museum collection* – the client hides page requests behind a plain ``for`` loop, exactly like database cursors and cloud SDK paginators do.

## Syllabus deliverables
> \_\_iter\_\_, \_\_next\_\_, and custom iterators

| Deliverable | Implemented in |
|---|---|
| ✅ \_\_iter\_\_ and \_\_next\_\_ | `PageCursor` |
| ✅ StopIteration ends the loop | `PageCursor.__next__` |
| ✅ custom iterator with state | `Countdown` |
| ✅ iterable vs iterator (re-iterable container) | `Collection` |
| ✅ what a for loop really does | `manual_for_loop` |
| ✅ iter(callable, sentinel) | `read_until_sentinel` |
| ✅ next() with a default | `first_match` |

## Key learnings
- An *iterable* returns a fresh iterator from `__iter__`; an *iterator* returns itself and is consumed once.
- `for` is sugar for `iter()` + repeated `next()` until `StopIteration`.
- `iter(callable, sentinel)` and `next(it, default)` remove most manual try/except around iteration.

## Pitfalls I hit (and how I fixed them)
- The first cursor popped items out of the collection's own page lists, so every later loop came back empty – iterators must copy or index, never consume shared data.

## Run it
```bash
python -m src.day_64_iterators_iterator_protocol.main
pytest tests/test_day_64.py -v
```

## Next step
- Replace the hand-written iterator with a generator function on Day 65.
