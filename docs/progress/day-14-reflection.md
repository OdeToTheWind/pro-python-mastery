# Day 14 - Code Blocks and Indentation Reflection

**Date:** 2026-03-26  
**Python Version Used:** 3.14  
**Time Spent:** ~2 hours  

## What I Built / Key Deliverables
- Interactive Indentation Explorer showing correct vs broken blocks
- Multiple demos: menu with proper if-elif, nested loops, pyramid patterns
- Clear cheat sheet explaining Python's indentation rules
- Practical exercises to spot and fix common IndentationError cases
- Unit tests validating block logic (if, for, nested structures)

## Core Learnings & Insights
- Python uses **indentation** (not curly braces) to define code blocks
- 4 spaces is the official standard (PEP 8)
- Never mix tabs and spaces — this is the #1 cause of IndentationError
- Every colon `:` starts a new block that must be indented
- Blocks can be nested (if inside for, for inside while, etc.)
- Consistent indentation makes code readable and prevents bugs

## Challenges Faced & How I Solved Them
- Making a "boring" topic engaging → turned it into interactive fixes and mini challenges
- Showing real errors without breaking the program → used try/except around user input
- Teaching nested blocks visually → star pyramid and nested if examples
- Testing indentation logic → created small pure functions that mimic block behavior

## Improvements for Next Time / Future Ideas
- Visual indentation highlighter (if using rich library)
- "Spot the bug" game with deliberately broken code snippets
- Compare with other languages (Python vs JavaScript/C++ braces)

## References / Resources Used
- PEP 8 – Style Guide for Python Code (Indentation section)
- Python docs: https://docs.python.org/3/reference/compound_stmts.html
- Real Python: Python Indentation Guide

## Self-Assessment
- Test coverage: ~80%
- Code cleanliness: Very high – strict 4-space indentation throughout
- Interactivity: Good – users actively practice and fix indentation
- Educational value: Critical foundational skill reinforced
- Personal rating: 9.0/10 – Essential day done properly

Day 14 complete — you now respect and master Python's indentation rules.  
Next: While Loops (Day 15).
