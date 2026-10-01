# Day 65 – Generators & yield Reflection

**Date:** 2026-10-01 · **Level:** Advanced · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_65_generators_yield/main.py`](../../src/day_65_generators_yield/main.py) · **Tests:** [`tests/test_day_65.py`](../../tests/test_day_65.py) (9 tests)

## Scenario
A *smart-meter energy monitor* that streams millions of readings. Generators process them one at a time, so memory stays flat no matter how large the stream is.

## Syllabus deliverables
> Generator functions, lazy evaluation, and memory benefits

| Deliverable | Implemented in |
|---|---|
| ✅ generator function with yield | `meter_readings` |
| ✅ infinite generator + islice | `meter_readings` |
| ✅ lazy evaluation (proved with a log) | `traced_readings` |
| ✅ generator expression | `kwh_total` |
| ✅ generator state is paused between yields | `peak_detector` |
| ✅ memory benefits (getsizeof) | `container_sizes` |
| ✅ memory benefits (tracemalloc) | `peak_memory_kib` |
| ✅ generators are single-use | `single_use_demo` |

## Key learnings
- A function containing `yield` returns a generator; its body runs only when `next()` asks for a value.
- Generators pause with their local variables intact, which makes stateful streams (spike detection) simple.
- Memory stays constant: a generator object is ~200 bytes whatever the stream length, a list grows with it.

## Pitfalls I hit (and how I fixed them)
- A generator can be consumed only once – a second `sum()` over it silently returns 0.

## Run it
```bash
python -m src.day_65_generators_yield.main
pytest tests/test_day_65.py -v
```

## Next step
- Chain generators into pipelines and send values into them on Day 66.
