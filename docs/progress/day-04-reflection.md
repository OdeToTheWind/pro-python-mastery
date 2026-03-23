# Day 04 – Variable Naming Rules – Reflection

**Date:** 2026-03-16

**What I learned / noticed today:**

- Strict syntax rules: start with letter or _, only alphanum + _, no keywords
- PEP 8 strongly recommends **snake_case** for variables & functions
- Descriptive names >> short names (readability wins in large projects)
- Single-letter variables are acceptable only in very local scope (loops)
- Never shadow built-ins (list, str, dict, type, max, sum, id, …)
- Leading underscore = "this is private / internal" (just convention)

**Challenges / mistakes I made:**

- Tried camelCase at first → looks nice but not Pythonic
- Almost used `list` as variable name → would break built-in list()

**Aha moment:**

Realized how much better `student_final_score` is than `s` or `x`

**Next day preview (Day 5):**
Probably data types or basic operators – looking forward to it!

**Commit message suggestion:**
"day_04: interactive variable naming rules + PEP 8 style + tests"