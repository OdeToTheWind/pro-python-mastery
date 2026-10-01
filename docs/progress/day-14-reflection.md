# Day 14 – Code Blocks and Indentation Reflection

**Date:** 2026-03-26 · **Level:** Beginner · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_14_code_block_indentation/main.py`](../../src/day_14_code_block_indentation/main.py) · **Tests:** [`tests/test_day_14.py`](../../tests/test_day_14.py) (7 tests)

## Scenario
A *snippet linter for a coding bootcamp* – students paste code and the tool compiles it, explains indentation errors and offers an automatic fix.

## Syllabus deliverables
> Python indentation rules, loop and function blocks, common IndentationError fixes

| Deliverable | Implemented in |
|---|---|
| ✅ indentation rules (compile check) | `check_snippet` |
| ✅ loop and function blocks | `block_outline` |
| ✅ IndentationError / TabError fixes | `fix_tabs` |
| ✅ catalogue of common errors | `BROKEN_SNIPPETS` |

## Key learnings
- `compile()` checks code without running it – perfect for linting snippets.
- `TabError` is a subclass of `IndentationError`, which is a subclass of `SyntaxError`, so order the `except` clauses from specific to general.
- Different blocks may use different (consistent) indentation; only lines in the same block must match.

## Pitfalls I hit (and how I fixed them)
- Expanding tabs to 4 spaces created a new indentation error – the tokenizer measures tabs to multiples of 8.

## Run it
```bash
./propython.sh 14                 # study mode: explanation, code map, notes and tests
python -m src.day_14_code_block_indentation.main
pytest tests/test_day_14.py -v
```

## Next step
- Let `ruff format` own indentation in every future file.
