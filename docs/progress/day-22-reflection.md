# Day 22 – Docstrings vs. Comments Reflection

**Date:** 2026-04-03 · **Level:** Beginner · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_22_doc_string_vs_comments/main.py`](../../src/day_22_doc_string_vs_comments/main.py) · **Tests:** [`tests/test_day_22.py`](../../tests/test_day_22.py) (8 tests)

## Scenario
A *kitchen unit-conversion library* that is documented properly and a documentation auditor that inspects it.

## Syllabus deliverables
> # comments vs """ docstrings, documentation standards and metadata

| Deliverable | Implemented in |
|---|---|
| ✅ docstrings (PEP 257, Google style) | `grams_to_cups` |
| ✅ comments vs docstrings at runtime | `split_comments_and_docstrings` |
| ✅ documentation standards check | `audit_docstring` |
| ✅ function metadata | `function_metadata` |

## Key learnings
- Comments are dropped by the compiler; docstrings live on as `__doc__` and power `help()` and IDEs.
- `inspect.getdoc` dedents docstrings; `inspect.signature` and `get_annotations` expose metadata.
- Docstring examples can run as doctests, so documentation can't silently rot.

## Pitfalls I hit (and how I fixed them)
- The tokenizer is the reliable way to separate comments from string literals – regex gets fooled.

## Run it
```bash
python -m src.day_22_doc_string_vs_comments.main
pytest tests/test_day_22.py -v
```

## Next step
- Generate API docs from these docstrings when packaging on Day 96.
