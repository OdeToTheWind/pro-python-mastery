# Day 23 - Scope and Local/Global Variables Reflection

**Date:** 2026-04-04   
**Python Version Used:** 3.14  
**Time Spent:** ~2.5 hours  

## What I Built / Key Deliverables
- Interactive Scope Explorer demonstrating LEGB rule
- Examples of local, enclosing, global, and built-in scopes
- Practical use of `global` and `nonlocal` keywords
- Demonstration of why global variables are dangerous
- Clear LEGB rule visualization

## Core Learnings & Insights
- Python follows the **LEGB** rule when looking for variables
- Local variables are created inside functions and destroyed when function ends
- `global` keyword allows modification of module-level variables
- `nonlocal` keyword allows modification of variables in enclosing (nested) functions
- Overusing global variables leads to hard-to-debug code and poor design
- Best practice: Pass data as parameters and return results instead of using globals

## Challenges Faced & How I Solved Them
- Making scope visible → created live demos showing variable values in different scopes
- Explaining `nonlocal` clearly → used nested counter example
- Showing dangers of globals → dedicated "why global variables are dangerous" demo
- Testing scope behavior → used small pure functions for pytest

## Improvements for Next Time / Future Ideas
- Closure examples (functions returning functions with nonlocal)
- Global variable refactoring exercise
- Scope in classes (instance vs class variables preview)

## References / Resources Used
- Python docs: https://docs.python.org/3/reference/executionmodel.html
- Real Python: Python Scope & LEGB Rule Guide

## Self-Assessment
- Test coverage: ~85%
- Code cleanliness: High – clear demonstrations of scope rules
- Interactivity: Excellent – users experiment with different scopes live
- Educational value: Very high – critical concept for avoiding bugs
- Personal rating: 9.3/10 – Important foundational topic completed

Day 23 complete — you now understand variable scope deeply.  
Next: Debugging Techniques (Day 24) - final day of Beginner Projects!
