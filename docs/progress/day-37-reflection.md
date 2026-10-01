# Day 37 – Python Turtle Reflection

**Date:** 2026-04-18 · **Level:** Intermediate · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_37_python_turtle/main.py`](../../src/day_37_python_turtle/main.py) · **Tests:** [`tests/test_day_37.py`](../../tests/test_day_37.py) (9 tests)

## Scenario
A *greeting-card artist* – draws shapes, a star burst, a spiral and an animated orbit with ``turtle``.

## Syllabus deliverables
> Graphics, shapes, drawing logic and animations using Turtle

| Deliverable | Implemented in |
|---|---|
| ✅ graphics setup | `main` |
| ✅ shapes: regular polygons | `draw_polygon` |
| ✅ shapes: stars | `draw_star` |
| ✅ drawing logic: angles | `exterior_angle` |
| ✅ drawing logic: spiral | `draw_spiral` |
| ✅ animation frames | `orbit_positions` |
| ✅ animation loop with ontimer | `animate_orbit` |

## Key learnings
- A regular polygon turns by `360 / sides`; a single-stroke star by `180 - 180 / points`.
- Passing the pen in as a protocol makes drawing logic testable without a window.
- `tracer(0)` plus `ontimer` gives smooth, non-blocking animation.

## Pitfalls I hit (and how I fixed them)
- Leaving the window open after an exception was fixed with `finally: turtle.bye()`.

## Run it
```bash
python -m src.day_37_python_turtle.main
pytest tests/test_day_37.py -v
```

## Next step
- Use the same pre-computed-frame approach for simulations on Day 98.
