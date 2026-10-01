# Day 72 – Advanced Typing Reflection

**Date:** 2026-10-01 · **Level:** Advanced · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_72_advanced_typing/main.py`](../../src/day_72_advanced_typing/main.py) · **Tests:** [`tests/test_day_72.py`](../../tests/test_day_72.py) (11 tests)

## Scenario
A *warehouse-robot fleet manager*. Robots from different vendors share no base class, yet the dispatcher accepts any of them because they satisfy a ``Protocol``. Payloads from the vendors' JSON APIs are described with ``TypedDict``; commands are restricted with ``Literal``; a generic repository works for robots, shelves or anything with an ``id``.

## Syllabus deliverables
> Protocol, TypeVar, Generic, TypedDict, Literal, and checking with mypy/pyright

| Deliverable | Implemented in |
|---|---|
| ✅ Protocol (structural typing) | `Movable` |
| ✅ runtime\_checkable Protocol | `HasBattery` |
| ✅ TypeVar bound to a Protocol | `closest` |
| ✅ constrained TypeVar | `scale` |
| ✅ Generic class | `Repository` |
| ✅ TypedDict with NotRequired | `RobotPayload` |
| ✅ Literal types | `Command` |
| ✅ Final constants | `MAX_SPEED` |
| ✅ checking with mypy | `type_check` |
| ✅ checking with pyright (optional) | `type_check` |

## Key learnings
- A `Protocol` checks structure, not inheritance – unrelated vendor classes satisfy it if they have the right members.
- A bounded `TypeVar` keeps the precise type flowing through a function; a constrained one allows only listed types.
- `TypedDict` and `Literal` describe JSON payloads and allowed strings so mypy can catch mistakes before runtime.

## Pitfalls I hit (and how I fixed them)
- `from __future__ import annotations` stops `NotRequired` from being seen at runtime inside a `TypedDict`, so the key was reported as required.

## Run it
```bash
./propython.sh 72                 # study mode: explanation, code map, notes and tests
python -m src.day_72_advanced_typing.main
pytest tests/test_day_72.py -v
```

## Next step
- Use these types to describe thread-safe workers on Day 73.
