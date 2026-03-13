# Day 02 - String Manipulation Reflection

**Date:** 2026-03-14  
**Python Version Used:** 3.14  
**Time Spent:** ~2 hours  

## What I Built / Key Deliverables
- Professional profile generator function with input cleaning and formatted output
- Used f-strings with alignment, padding, and centering
- Unit tests covering messy input, edge cases (empty name, zero years)
- Runnable demonstration in main.py

## Core Learnings & Insights
- `str.strip().title()` combo is perfect for name normalization
- f-string specifiers like `:<20`, `:^30`, `:02` make alignment trivial and readable
- Slicing + formatting = quick & safe way to build handles/usernames
- `upper()` vs `title()` — important distinction for roles vs names
- Keeping functions pure (no print inside) makes them testable/reusable

## Challenges Faced & How I Solved Them
- Alignment looked off with long names → switched to fixed-width + truncation if needed (future improvement)
- Wanted to avoid hard-coded widths → considered dynamic calculation but kept simple for Day 2

## Improvements for Next Time / Future Ideas
- Add truncation or ellipsis for very long names
- Support multi-line output or rich console (rich library?)
- Validate years (positive int) with better error messages
- Extend to generate Markdown/JSON versions of the profile

## References / Resources Used
- Python docs: str methods (strip, title, upper, format specifiers)
- Real Python: "f-strings in Python"
- PEP 498 – Literal String Interpolation

## Self-Assessment
- Test coverage: High for core logic (~95%)
- Typing: Good – inputs/outputs annotated
- Code cleanliness: Very readable, single responsibility
- Personal rating: 9/10 – enjoyable day, output looks professional