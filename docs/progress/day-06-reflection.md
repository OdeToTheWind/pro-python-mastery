# Day 06 - Data Types Reflection

**Date:** 2026-03-18  
**Python Version Used:** 3.14  
**Time Spent:** ~2–3 hours  

## What I Built / Key Deliverables
- Interactive data type explorer: user enters values → shows type, mutability, hashability, ID, length, type-specific previews
- Safe literal evaluation with `ast.literal_eval()` (handles int/float/bool/list/tuple/dict/set/None safely)
- Fallback to `str` for non-literal input
- Printed overview table: categories, mutability, ordering, hashability
- Quit support at any time (consistent with previous days)
- Basic type-specific demonstrations (upper for str, keys for dict, etc.)

## Core Learnings & Insights
- Python is **dynamically typed** — types determined at runtime, no declaration needed
- **Immutable** types (int, float, bool, str, tuple, frozenset, bytes): cannot change → safe for keys/sets
- **Mutable** types (list, dict, set, bytearray): can be modified in-place → careful with shared references
- `type()` gives exact class; `isinstance()` better for checking (supports inheritance)
- `ast.literal_eval()` = safe way to parse user input into Python literals (no code execution risk)
- `id()` shows object identity — same value immutable objects often share ID, mutable usually don't
- Collections have different ordering guarantees: dicts insertion-ordered since 3.7, sets unordered
- `None` is singleton — always same object (`is None` is preferred over `== None`)

## Challenges Faced & How I Solved Them
- Safe parsing of user input → used `ast.literal_eval()` instead of `eval()` (security!)
- Handling quit consistently → return `None` from input helper + check after each call
- Displaying useful type-specific info without too much complexity → simple `isinstance()` branches
- Making table readable in console → used fixed-width separators and alignment
- Wanted to support complex literals but keep safety → `literal_eval` covers most beginner cases

## Improvements for Next Time / Future Ideas
- Add type conversion playground: "convert this to list / int / str"
- Show memory usage (`sys.getsizeof()`) for different types
- Mini quiz: "what type is this?", "is this mutable?", etc.
- Support more advanced literals (complex numbers: 3+4j)
- Color output with `rich` or ANSI for better visual distinction
- Add `repr()` vs `str()` demonstration

## References / Resources Used
- Official docs: https://docs.python.org/3/library/stdtypes.html
- PEP 8 & Python typing best practices
- Real Python: Python Data Types articles
- ast.literal_eval docs (safety emphasis)

## Self-Assessment
- Test coverage: ~70–80% (literal_eval behavior covered; I/O harder to test without mocks)
- Code cleanliness: Modular, safe, readable, good comments
- Interactivity: Very engaging — users experiment freely with different inputs
- Educational value: Strong overview + hands-on discovery
- Personal rating: 9/10 – Excellent bridge from basics to collections & mutability

Day 6 done — data types feel much more concrete now.  
Next: probably lists & tuples in depth, or booleans + comparisons + if-statements.