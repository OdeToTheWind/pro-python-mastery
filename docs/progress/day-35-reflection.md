# Day 35 – Event Listeners Reflection

**Date:** 2026-04-16 · **Level:** Intermediate · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_35_event_listeners/main.py`](../../src/day_35_event_listeners/main.py) · **Tests:** [`tests/test_day_35.py`](../../tests/test_day_35.py) (10 tests)

## Scenario
A *smart-home hub*. Devices emit events (doorbell rang, motion detected); any number of independent listeners react without the devices knowing who is listening.

## Syllabus deliverables
> Event-driven patterns and callback-based interactions

| Deliverable | Implemented in |
|---|---|
| ✅ event-driven pattern (publish/subscribe) | `EventBus` |
| ✅ callbacks | `EventBus.on` |
| ✅ unsubscribe | `EventBus.off` |
| ✅ one-shot listeners | `EventBus.once` |
| ✅ decorator registration | `EventBus.listener` |
| ✅ error isolation between listeners | `EventBus.emit` |
| ✅ devices that emit events | `Doorbell` |

## Key learnings
- Publish/subscribe decouples the event source from the reactions.
- One failing listener must not stop the others – isolate and record errors.
- `once`, `off` and priorities cover most real event-bus needs.

## Pitfalls I hit (and how I fixed them)
- An unsubscribe lambda returned a bool; a named inner function made the contract clear.

## Run it
```bash
./propython.sh 35                 # study mode: explanation, code map, notes and tests
python -m src.day_35_event_listeners.main
pytest tests/test_day_35.py -v
```

## Next step
- Make the event bus asynchronous on Day 75.
