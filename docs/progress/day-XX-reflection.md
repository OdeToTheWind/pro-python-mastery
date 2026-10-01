# Day XX – [Topic from syllabus.md] Reflection

> Template for new days. You don't edit the finished reflection by hand:
> 1. add `src/day_XX_<topic>/main.py` with a module docstring containing
>    `Scenario: ...` and a `DELIVERABLES = {"deliverable": "function_or_class"}` map
>    that covers every item in the syllabus row,
> 2. add `tests/test_day_XX.py` that imports and exercises that module,
> 3. add `docs/progress/notes/day-XX.json`:
>    ```json
>    {"date": "YYYY-MM-DD",
>     "learnings": ["…", "…", "…"],
>     "pitfalls": ["…"],
>     "next": "…"}
>    ```
> 4. mark the day **Covered** in `syllabus.md` and run `python scripts/build_reflections.py`.
>
> `tests/test_syllabus_sync.py` fails CI if any of these pieces is missing or out of sync.

**Date:** YYYY-MM-DD · **Level:** Beginner/Intermediate/Advanced/Capstone · **Python:** 3.12+ · **Status:** Covered
**Code:** `src/day_XX_<topic>/main.py` · **Tests:** `tests/test_day_XX.py` (N tests)

## Scenario
One sentence: the realistic situation this day's code models.

## Syllabus deliverables
> Copied verbatim from the syllabus row.

| Deliverable | Implemented in |
|---|---|
| ✅ … | `function_or_class` |

## Key learnings
- …

## Pitfalls I hit (and how I fixed them)
- …

## Run it
```bash
python -m src.day_XX_<topic>.main
pytest tests/test_day_XX.py -v
```

## Next step
- …
