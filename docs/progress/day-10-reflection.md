# Day 10 – Randomisation Reflection

**Date:** 2026-03-22 · **Level:** Beginner · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_10_randomisation/main.py`](../../src/day_10_randomisation/main.py) · **Tests:** [`tests/test_day_10.py`](../../tests/test_day_10.py) (14 tests)

## Scenario
A *board-game night toolkit* – dice, a card deck, a raffle and a password generator for the Wi-Fi.

## Syllabus deliverables
> random module, randint(), choice(), shuffle(), password generation, games

| Deliverable | Implemented in |
|---|---|
| ✅ randint() | `roll_dice` |
| ✅ shuffle() | `deal_cards` |
| ✅ choice() | `pick_raffle_winner` |
| ✅ seeding for reproducibility | `roll_dice` |
| ✅ secure password generation | `generate_password` |
| ✅ game | `rock_paper_scissors` |

## Key learnings
- Inject `random.Random(seed)` so randomness is reproducible in tests without touching global state.
- `secrets` (a CSPRNG) is required for passwords; `random` is predictable.
- `shuffle` works in place and returns `None`.

## Pitfalls I hit (and how I fixed them)
- `randint(1, 0)` raises `ValueError` – dice now validate their sides.

## Run it
```bash
./propython.sh 10                 # study mode: explanation, code map, notes and tests
python -m src.day_10_randomisation.main
pytest tests/test_day_10.py -v
```

## Next step
- Use seeded RNGs for the Monte Carlo capstone on Day 98.
