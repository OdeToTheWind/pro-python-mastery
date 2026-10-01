# Day 38 – Game Development with Python and OOP Reflection

**Date:** 2026-04-19 · **Level:** Intermediate · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_38_game_development_with_python_and_oop/main.py`](../../src/day_38_game_development_with_python_and_oop/main.py) · **Tests:** [`tests/test_day_38.py`](../../tests/test_day_38.py) (9 tests)

## Scenario
*Dungeon Duel* – a turn-based battle between a hero and monsters. Both sides attack, the hero can heal with limited potions, and the battle can be won **or lost**. Randomness is injected so games are reproducible in tests.

## Syllabus deliverables
> Simple game-building using classes, state and user interaction

| Deliverable | Implemented in |
|---|---|
| ✅ game classes | `Character` |
| ✅ player-specific behaviour | `Hero` |
| ✅ game state and turn logic | `Battle` |
| ✅ enemy AI (counter-attacks) | `Battle.enemy_turn` |
| ✅ user interaction loop | `play` |

## Key learnings
- Game state (HP, potions, turn log, winner) belongs in objects, not loose variables.
- Injected randomness makes a whole battle reproducible in a test.
- A game the player can't lose is not a game – the enemy now strikes back.

## Pitfalls I hit (and how I fixed them)
- Clamping damage at zero HP prevents negative health and weird win states.

## Run it
```bash
./propython.sh 38                 # study mode: explanation, code map, notes and tests
python -m src.day_38_game_development_with_python_and_oop.main
pytest tests/test_day_38.py -v
```

## Next step
- Add save/load of a battle with Day 53's persistence.
