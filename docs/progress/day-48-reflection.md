# Day 48 – Creating Desktop GUI Apps with Tkinter Reflection

**Date:** 2026-04-29 · **Level:** Intermediate · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_48_tkinter_gui/main.py`](../../src/day_48_tkinter_gui/main.py) · **Tests:** [`tests/test_day_48.py`](../../tests/test_day_48.py) (5 tests)

## Scenario
A *restaurant tip splitter* desktop app. The calculation is a pure function (unit-tested everywhere); the GUI is a thin layer of widgets laid out with ``grid`` that reads user input and shows results or errors.

## Syllabus deliverables
> GUI building with widgets, layouts and user input

| Deliverable | Implemented in |
|---|---|
| ✅ widgets | `TipApp.build` |
| ✅ grid layout | `TipApp.build` |
| ✅ user input handling | `TipApp.calculate` |
| ✅ input validation (pure, testable) | `calculate_tip` |
| ✅ event binding | `TipApp.build` |

## Key learnings
- Keep the calculation pure and the widgets thin – the logic is testable without a display.
- `grid` with `sticky` and `columnconfigure` makes layouts resize well.
- Tk variables (`StringVar`, `IntVar`) connect widgets to Python state.

## Pitfalls I hit (and how I fixed them)
- Importing `tkinter` at module level made the app crash before its fallback could run.

## Run it
```bash
python -m src.day_48_tkinter_gui.main
pytest tests/test_day_48.py -v
```

## Next step
- Explore a modern UI alternative (Textual or a web front end) after the capstone.
