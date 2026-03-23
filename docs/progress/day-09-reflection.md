# Day 09 - Logical Operations (and / or / not) Reflection

**Date:** 2026-03-21  
**Python Version Used:** 3.14  
**Time Spent:** ~2–2.5 hours  

## What I Built / Key Deliverables
- Interactive eligibility/access checker using combined logical conditions
- Truth table printout + short-circuit behavior demo
- Safe input helpers (int/float/yes-no) with quit support
- Bonus: limited "try your own expression" playground (safe eval with restricted globals)
- Unit tests on the core decision function (eligibility_check)

## Core Learnings & Insights
- `and` returns the last evaluated argument (short-circuits on falsy left)
- `or` returns the first truthy argument (short-circuits on truthy left)
- `not` simply inverts — not falsy = truthy
- Truthy/falsy applies to all objects, not just booleans
- Logical ops have lower precedence than comparisons → use parentheses for clarity
- Short-circuiting is useful for guard clauses (e.g. `user and user.is_active`)
- Combining with `if` creates powerful decision trees without deep nesting

## Challenges Faced & How I Solved Them
- Explaining short-circuit without confusion → live print examples
- Safe "eval" for user expressions → restricted globals + builtins empty
- Making inputs robust → generic safe_input with type_cast
- Keeping program engaging → real-world eligibility scenario + instant feedback

## Improvements for Next Time / Future Ideas
- Add more scenarios (login validator, discount calculator, password strength)
- Quiz mode: predict outcome of expression → check answer
- Visualize truth table interactively (user inputs A/B)
- Use `rich` for colored truth table + results
- Expand tests: short-circuit side-effect checks (mock print)

## References / Resources Used
- Python docs: https://docs.python.org/3/reference/expressions.html#boolean-operations
- Real Python / GeeksforGeeks / W3Schools logical operators articles
- freeCodeCamp: Truthy and Falsy Values in Python

## Self-Assessment
- Test coverage: ~85% on decision logic
- Code cleanliness: Modular, safe, readable, consistent UX
- Interactivity: Good mix of guided + free experimentation
- Educational value: Clear progression from basics to combined conditions
- Personal rating: 9.1/10 – Solid bridge from conditionals to more complex logic

Day 9 done — logical combinations feel natural now.  
Next: likely while loops, for loops, or range().