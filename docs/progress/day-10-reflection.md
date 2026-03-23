# Day 10 - Randomisation Reflection

**Date:** 2026-03-22  
**Python Version Used:** 3.14  
**Time Spent:** ~2–2.5 hours  

## What I Built / Key Deliverables
- Interactive randomisation playground with multiple mini-tools/games:
  - Coin flip
  - Custom dice roller
  - Rock-Paper-Scissors vs computer
  - Random password generator
  - Random choice from user list
  - Seed reproducibility demo
- Clear cheat sheet / reference table for `random` module functions
- Safe, user-driven inputs (no hard-coded values)
- Basic unit tests for core random functions

## Core Learnings & Insights
- `random` module provides pseudo-random numbers (not cryptographically secure)
- `random.seed()` makes results reproducible → great for testing / demos
- `random.random()` → float [0.0, 1.0)
- `random.randint(a,b)` → inclusive range
- `random.choice()` → one item, `random.choices()` → multiple with replacement
- `random.shuffle()` modifies list in-place
- Most games, simulations, sampling, and testing rely heavily on randomness
- Never use `random` for passwords, tokens, nonces → use `secrets` module

## Challenges Faced & How I Solved Them
- Making randomness feel interactive → created multiple small games/tools
- Explaining seed behavior → added live reproducibility demo
- Avoiding repetitive code → used helper functions for each activity
- Keeping UX friendly → menu-driven with quit support

## Improvements for Next Time / Future Ideas
- Add weighted random choice (`random.choices` with weights)
- Number guessing game (higher/lower hints)
- Random quote / joke generator (small list)
- Monte Carlo simulation example (e.g. pi approximation)
- Use `secrets` module demo for contrast (secure random)

## References / Resources Used
- Python docs: https://docs.python.org/3/library/random.html
- Real Python: Python random module guide
- GeeksforGeeks / W3Schools random articles

## Self-Assessment
- Test coverage: ~80% (core functions tested)
- Code cleanliness: Modular, readable, consistent UX
- Interactivity: High — many ways to play/experiment
- Educational value: Strong – covers most common use cases
- Personal rating: 9.0/10 – Fun day, very practical topic

Day 10 complete — randomness is now under control.  
Next: Error Handling (try/except, raising exceptions, etc.).