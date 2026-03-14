# Day 03 - Input and Print Functions Reflection

**Date:** 2026-03-15  
**Python Version Used:** 3.14  
**Time Spent:** ~2–3 hours  

## What I Built / Key Deliverables
- Interactive profile builder using `input()` with validation loop
- Reusable `get_validated_input()` helper with type conversion & min-value check
- Formatted profile output using f-strings (alignment, precision, expressions)
- Unit tests mocking input for reliable testing

## Core Learnings & Insights
- `input()` always returns `str` → mandatory type conversion (`int()`, `float()`) + error handling
- Validation loops prevent crashes from bad input (ValueError, empty, below min)
- `print()` advanced features: `sep`, `end`, f-string format specifiers (`:<`, `:>`, `:.1f`, `:+d`)
- Mocking `input()` with `unittest.mock.patch` makes console code testable
- Separation of concerns: input collection vs formatting/display

## Challenges Faced & How I Solved Them
- Handling invalid inputs without infinite loops → used `while True` + `try/except`
- Testing interactive functions → `patch` + `side_effect` for multi-input simulation
- Making output look professional → experimented with widths, centering, dynamic messages

## Improvements for Next Time / Future Ideas
- Add more validation (email regex, choice from list)
- Use `rich` or `typer` for prettier console UI
- Save profile to JSON file
- Handle KeyboardInterrupt (Ctrl+C) gracefully

## References / Resources Used
- Python docs: input(), print(), f-strings (PEP 498)
- Real Python: Python print() Guide
- GeeksforGeeks: Input and Output in Python
- unittest.mock documentation

## Self-Assessment
- Test coverage: ~80–90% (focused on logic, not full UI)
- Typing: Good – helpers fully annotated
- Code cleanliness: Modular and readable
- Personal rating: 8.5/10 – Solid interactive foundation