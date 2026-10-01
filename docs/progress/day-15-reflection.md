# Day 15 – While Loops Reflection

**Date:** 2026-03-27 · **Level:** Beginner · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_15_while_loops/main.py`](../../src/day_15_while_loops/main.py) · **Tests:** [`tests/test_day_15.py`](../../tests/test_day_15.py) (13 tests)

## Scenario
An *arcade cabinet* – a number-guessing game, a PIN lock and a coin-counting machine, each driven by ``while`` loops.

## Syllabus deliverables
> while loops, break, continue, while-else, input validation and games

| Deliverable | Implemented in |
|---|---|
| ✅ while loop | `collatz_steps` |
| ✅ break | `guessing_game` |
| ✅ continue | `count_coins` |
| ✅ while ... else | `unlock` |
| ✅ input validation loop | `ask_int` |
| ✅ game | `guessing_game` |
| ✅ safe calculator (replaces eval) | `safe_eval` |

## Key learnings
- `while` fits loops whose iteration count is unknown in advance (Collatz, retries, games).
- `continue` skips the rest of one iteration; `break` leaves the loop; `while ... else` detects 'no break'.
- An AST walker with an operator whitelist is a safe calculator; `eval` with empty builtins is not.

## Pitfalls I hit (and how I fixed them)
- The original calculator could be escaped with `().__class__.__base__.__subclasses__()` – it was replaced.

## Run it
```bash
./propython.sh 15                 # study mode: explanation, code map, notes and tests
python -m src.day_15_while_loops.main
pytest tests/test_day_15.py -v
```

## Next step
- Revisit AST processing when building the data-validation library on Day 94.
