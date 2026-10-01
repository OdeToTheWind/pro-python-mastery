# Day 26 – PyCharm Tips and Tricks Reflection

**Date:** 2026-04-07 · **Level:** Intermediate · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_26_pycharm_tips_tricks/main.py`](../../src/day_26_pycharm_tips_tricks/main.py) · **Tests:** [`tests/test_day_26.py`](../../tests/test_day_26.py) (8 tests)

## Scenario
A *pocket IDE coach* – a searchable shortcut cheat-sheet per OS, a live-template expander and a safe "Rename" refactoring that works the way the IDE's does (on tokens, not on raw text).

## Syllabus deliverables
> IDE productivity, debugging, refactoring tools, templates and shortcuts

| Deliverable | Implemented in |
|---|---|
| ✅ IDE productivity / shortcuts | `find_shortcuts` |
| ✅ debugging tools | `SHORTCUTS` |
| ✅ refactoring tools (Rename) | `safe_rename` |
| ✅ live templates | `expand_template` |
| ✅ cheat sheet | `cheat_sheet` |

## Key learnings
- Rename refactoring must work on tokens; text replace also changes strings, comments and longer names.
- Live templates are parameterised snippets – the same idea as `string.Template`.
- Learning a few navigation and debugger shortcuts saves more time than any plugin.

## Pitfalls I hit (and how I fixed them)
- Numbering items by hand *and* with `enumerate` printed `1. 1.` – number in one place only.

## Run it
```bash
./propython.sh 26                 # study mode: explanation, code map, notes and tests
python -m src.day_26_pycharm_tips_tricks.main
pytest tests/test_day_26.py -v
```

## Next step
- Practise the debugger shortcuts on Day 24's buggy payroll script.
