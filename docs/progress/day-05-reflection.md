# Day 05 - Mathematical Operations Reflection

**Date:** 2026-03-17  
**Python Version Used:** 3.14  
**Time Spent:** ~2–2.5 hours  

## What I Built / Key Deliverables
- Interactive arithmetic calculator using all main operators (+ - * / // % **)
- Safe input helper `safe_float_input()` with validation loop & ValueError handling
- `perform_operation()` function with safe division-by-zero protection
- Clear operator reference table (printed) showing name, example, result, notes
- Real-time feedback with operator description + nice formatting of results
- Unit tests covering normal cases, floor/mod/div edge cases, zero division

## Core Learnings & Insights
- `/` always returns **float**, even when dividing integers (Python 3 behavior)
- `//` = floor division → rounds down toward negative infinity (not just truncate)
- `%` = remainder → sign follows the divisor (useful for cycles, even/odd checks)
- `**` = exponentiation, right-associative (2 ** 3 ** 2 = 2 ** (3 ** 2) = 512)
- Operator precedence: exponents first → then * / // % → then + - (left to right)
- Division/modulus by zero raises `ZeroDivisionError` → must check explicitly
- `float.is_integer()` helps clean output (show 8 instead of 8.0 when possible)

## Challenges Faced & How I Solved Them
- Handling division by zero gracefully → return tuple with "Error" string instead of crashing
- Making input robust → `while True` + `try/except ValueError` + empty check
- Testing floating-point results → used small tolerance (`1e-10`) instead of exact ==
- Wanted clean output for whole-number floats → conditional `int()` conversion
- Precedence confusion → added small bonus example showing parentheses importance

## Improvements for Next Time / Future Ideas
- Add more operators: `divmod()`, unary `-`, bitwise if relevant later
- Let user input full expression (eval() with safe restrictions — advanced)
- Add mini challenges: "make 24 with these 4 numbers", simple interest calc, BMI calculator
- Colorize output with ANSI or `rich` (green ✓, red ✗)
- Save favorite calculations to a list and show history at end

## References / Resources Used
- Python docs: https://docs.python.org/3/reference/expressions.html#arithmetic-conversions
- W3Schools / Programiz / GeeksforGeeks arithmetic operators pages
- Real Python: Python Operators article

## Self-Assessment
- Test coverage: ~90% (normal ops + zero-division + invalid op)
- Typing & structure: Clean, modular, well-annotated
- Interactivity: Very engaging — full user control over numbers & operations
- Code cleanliness: Readable, consistent formatting, good comments
- Personal rating: 9/10 – Strong interactive lesson + solid error handling + good tests

Day 5 done — arithmetic is now comfortable territory.  
Next: probably comparisons / booleans / conditionals.