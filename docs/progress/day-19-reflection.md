# Day 19 – Nested Collections Reflection

**Date:** 2026-03-31 · **Level:** Beginner · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_19_nested_collections/main.py`](../../src/day_19_nested_collections/main.py) · **Tests:** [`tests/test_day_19.py`](../../tests/test_day_19.py) (9 tests)

## Scenario
A *school gradebook* – classes contain students, students contain subjects, subjects contain lists of scores.

## Syllabus deliverables
> List of dicts, dict of lists, nested structures and classroom systems

| Deliverable | Implemented in |
|---|---|
| ✅ list of dicts (flat records) | `build_gradebook` |
| ✅ dict of lists (scores per subject) | `subject_scores` |
| ✅ nested structure access | `deep_get` |
| ✅ classroom system operations | `add_score` |
| ✅ reporting over nested data | `class_report` |

## Key learnings
- `setdefault` chains build nested dicts without `if key not in ...` ladders.
- Flipping nesting (class → student → subject into subject → scores) is a common reporting task.
- A `deep_get` helper keeps lookups into optional nested data safe.

## Pitfalls I hit (and how I fixed them)
- Copying the record lists is essential; shared inner lists leak changes between objects.

## Run it
```bash
./propython.sh 19                 # study mode: explanation, code map, notes and tests
python -m src.day_19_nested_collections.main
pytest tests/test_day_19.py -v
```

## Next step
- Analyse the same data with pandas on Day 44.
