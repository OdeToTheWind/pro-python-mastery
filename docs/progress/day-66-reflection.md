# Day 66 – Advanced Generators Reflection

**Date:** 2026-10-01 · **Level:** Advanced · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_66_advanced_generators/main.py`](../../src/day_66_advanced_generators/main.py) · **Tests:** [`tests/test_day_66.py`](../../tests/test_day_66.py) (13 tests)

## Scenario
An *online-shop order pipeline* – raw order lines flow through composable generator stages (parse → validate → enrich → batch), nested category trees are flattened with ``yield from``, and a live revenue tracker receives values via ``send()``.

## Syllabus deliverables
> yield from, generator pipelines, and sending values

| Deliverable | Implemented in |
|---|---|
| ✅ yield from: flattening nested data | `walk_categories` |
| ✅ yield from: capturing a return value | `count_and_forward` |
| ✅ pipeline stage: parse | `parse_lines` |
| ✅ pipeline stage: validate | `valid_orders` |
| ✅ pipeline stage: enrich | `with_tax` |
| ✅ pipeline stage: batch | `batched` |
| ✅ composed pipeline | `build_pipeline` |
| ✅ send() into a coroutine-style generator | `revenue_tracker` |
| ✅ throw() and close() | `revenue_tracker` |

## Key learnings
- `yield from` delegates to a sub-generator and captures its `return` value.
- Pipeline stages pull lazily from each other, so the first result arrives before the input is fully read.
- `send()` turns a generator into a coroutine-style consumer; it must be primed with `next()` first.

## Pitfalls I hit (and how I fixed them)
- Sending to an unprimed generator raises `TypeError`; `close()` and `throw()` are the clean ways to stop or signal it.

## Run it
```bash
python -m src.day_66_advanced_generators.main
pytest tests/test_day_66.py -v
```

## Next step
- Wrap pipeline stages with timing and retry decorators on Day 67.
