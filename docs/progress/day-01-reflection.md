# Day 01 - Variables, Type Hinting & Scoping Reflection

**Date:** 2026-03-13  
**Python Version Used:** 3.14  
**Time Spent:** ~2.5 hours  

## What I Built / Key Deliverables
- Simple main.py demonstrating variable declaration, reassignment, and basic logic
- Full function/type-hinted signatures
- Unit tests validating behavior under different inputs

## Core Learnings & Insights
- PEP 695 (new generic syntax in 3.12+) is clean but I stuck to classic `List[T]` style for compatibility
- Learned how Python's scoping rules (LEGB) interact with globals/nonlocal in nested functions
- f-strings are dramatically more readable than .format() or % — adopted as default
- Type hints make intent crystal clear and catch many bugs early via mypy

## Challenges Faced & How I Solved Them
- Initially forgot to annotate return types → mypy complained → added consistently
- One test failed due to mutable default argument trap → used None + if-check pattern

## Improvements for Next Time / Future Ideas
- Add property-based testing (hypothesis) for variables edge cases
- Explore __annotations__ introspection in runtime
- Maybe add a small CLI wrapper using typer or argparse

## References / Resources Used
- PEP 484 – Type Hints
- PEP 695 – Type Parameter Syntax (Python 3.12)
- Real Python: "Python Scope & the LEGB Rule"
- mypy documentation (quickstart)

## Self-Assessment
- Test coverage: ~85–90%
- Typing: Fully annotated (strict mode passes)
- Code cleanliness: Good, but could extract more helpers
- Personal rating: 8/10 – solid foundation, happy with typing discipline