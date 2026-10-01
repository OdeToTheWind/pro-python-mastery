# Day 70 – Metaclasses (Introduction) Reflection

**Date:** 2026-10-01 · **Level:** Advanced · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_70_metaclasses_intro/main.py`](../../src/day_70_metaclasses_intro/main.py) · **Tests:** [`tests/test_day_70.py`](../../tests/test_day_70.py) (11 tests)

## Scenario
A *document-converter app* with format plugins (Markdown → HTML, CSV → JSON …). Every plugin class must declare its formats and is registered automatically – first with a metaclass, then with the simpler ``__init_subclass__`` hook that is usually the better choice.

## Syllabus deliverables
> type, custom metaclasses, and when or when not to use them

| Deliverable | Implemented in |
|---|---|
| ✅ type is the class of classes | `type_facts` |
| ✅ creating a class dynamically with type() | `make_converter` |
| ✅ custom metaclass validating class definitions | `PluginMeta` |
| ✅ custom metaclass registering subclasses | `PluginMeta.registry` |
| ✅ simpler alternative: \_\_init\_subclass\_\_ | `Exporter` |
| ✅ metaclass conflicts (a reason to avoid them) | `metaclass_conflict` |
| ✅ decision guide | `WHEN_TO_USE` |

## Key learnings
- Classes are objects whose class is `type`; `type(name, bases, namespace)` creates classes at runtime.
- A metaclass's `__new__` runs at *class definition* time, so it can validate and register plugins before any instance exists.
- `__init_subclass__` covers most real use cases (registration, validation) without a metaclass.

## Pitfalls I hit (and how I fixed them)
- Combining two unrelated metaclasses raises a metaclass conflict – a strong reason to prefer simpler hooks.

## Run it
```bash
./propython.sh 70                 # study mode: explanation, code map, notes and tests
python -m src.day_70_metaclasses_intro.main
pytest tests/test_day_70.py -v
```

## Next step
- Use functional tools (`functools`, `itertools`) to simplify plugin logic on Day 71.
