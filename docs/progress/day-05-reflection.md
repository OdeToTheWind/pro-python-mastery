# Day 05 - Mathematical Operations Reflection

**Date:** 2026-03-17  
**Python Version Used:** 3.14  
**Time Spent:** ~2.5–3 hours  

## What I Built / Key Deliverables
- Fully interactive arithmetic playground covering all core operators (+ - * / // % **)
- `safe_float_input()` helper — robust number collection with quit support (`None` return on 'quit'/'q'/'exit')
- `perform_operation()` — safe dispatcher with zero-division protection and clear descriptions
- Printed quick-reference table for operators (name, example, result, notes)
- Real-time result feedback with clean formatting (convert float→int when whole number)
- Graceful exit from any input prompt without leftover questions
- Unit tests focused on `perform_operation()` (normal cases + zero-division + invalid ops)

## Core Learnings & Insights
- `/` always returns float (Python 3 true division)
- `//` floors toward -∞ (not just truncate toward zero)
- `%` remainder takes sign of divisor — useful for modular arithmetic patterns
- `**` is right-associative → `2 ** 3 ** 2 == 2 ** (3 ** 2) == 512`
- Precedence order: ** > * / // % > + -  (left-to-right for same level)
- Explicit zero-division checks are essential to avoid runtime crashes
- `float.is_integer()` + conditional `int()` conversion gives cleaner output (8 instead of 8.0)
- Early quit support in input loop greatly improves UX in interactive CLI tools

## Challenges Faced & How I Solved Them
- Initial quit logic only checked first number → operator prompt still appeared → fixed with `None` checks after **every** input call + proper `break`
- Duplicated/misplaced `op_input = input(...)` line after first-number quit check → removed duplicate, fixed control flow
- `safe_float_input` imported in tests but unused → normal (tests target logic, not I/O); could mock later if needed
- Floating-point comparison in tests → used small epsilon (`1e-10`) for safe equality
- Wanted smooth quit at any stage → made `safe_float_input` return `None` on quit keywords, checked after each call

## Improvements for Next Time / Future Ideas
- Add calculation history (store last 5–10 results, show on demand)
- Support more input styles (e.g. "5 + 3" full expression parsing — safe `eval` or manual parser)
- Mini-games/challenges: target number game, quick mental math quiz, unit conversions
- Add ANSI colors or `rich` for prettier ✓ / ✗ / table output
- Extend tests: mock `input()` to verify quit paths and full interaction flows
- Handle very large exponents gracefully (OverflowError → friendly message)

## References / Resources Used
- Python docs: https://docs.python.org/3/reference/expressions.html#arithmetic-conversions
- Python docs: https://docs.python.org/3/library/functions.html#quit (quit behavior inspiration)
- Real Python: Python Operator Precedence & Arithmetic
- PEP 8 & general CLI UX patterns for graceful exit

## Self-Assessment
- Test coverage: ~90% on core logic (`perform_operation`); I/O paths untested (intentional for now)
- Typing: Improved — `float | None` return type clearly communicates quit possibility
- Interactivity & UX: Much smoother with quit-at-any-point support
- Code cleanliness: Flow fixed, no duplication, readable & consistent
- Personal rating: 9.2/10 – Solid arithmetic foundation + professional-grade input handling + good resilience

Day 5 complete — arithmetic operators feel natural now, and the calculator is pleasant to use.  
Next up: likely comparison operators, booleans, and if/else conditionals.

Keep the momentum going! 🚀