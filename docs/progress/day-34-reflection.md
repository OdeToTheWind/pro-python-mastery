# Day 34 – Optional, Required and Default Parameters Reflection

**Date:** 2026-04-15 · **Level:** Intermediate · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_34_optional_required_default_parameters/main.py`](../../src/day_34_optional_required_default_parameters/main.py) · **Tests:** [`tests/test_day_34.py`](../../tests/test_day_34.py) (11 tests)

## Scenario
A *CI job scheduler* whose ``schedule_job`` signature uses every parameter kind Python offers, in the only order Python allows.

## Syllabus deliverables
> Advanced parameter handling, \*args, \*\*kwargs and ordering rules

| Deliverable | Implemented in |
|---|---|
| ✅ required vs optional parameters | `describe_parameters` |
| ✅ parameter ordering rules | `schedule_job` |
| ✅ \*args | `schedule_job` |
| ✅ \*\*kwargs | `schedule_job` |
| ✅ required keyword-only parameter | `schedule_job` |
| ✅ None sentinel vs mutable default | `add_label` |
| ✅ forwarding \*args/\*\*kwargs | `with_defaults` |

## Key learnings
- Parameter order is fixed: positional-only, `/`, standard, `*args`, keyword-only, `**kwargs`.
- A keyword-only parameter after `*args` can be required (no default).
- Wrappers forward `*args, **kwargs` to stay signature-agnostic.

## Pitfalls I hit (and how I fixed them)
- Illegal signatures are `SyntaxError`s at compile time – compiling them in a test proves the rules.

## Run it
```bash
python -m src.day_34_optional_required_default_parameters.main
pytest tests/test_day_34.py -v
```

## Next step
- Use `functools.wraps` with forwarding wrappers when writing decorators (Day 67).
