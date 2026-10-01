# Day 57 – REST APIs & JSON Reflection

**Date:** 2026-09-29 · **Level:** Advanced · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_57_rest_apis_json/main.py`](../../src/day_57_rest_apis_json/main.py) · **Tests:** [`tests/test_day_57.py`](../../tests/test_day_57.py) (11 tests)

## Scenario
A *to-do list REST API* simulated in memory. No network: the goal is to understand what HTTP methods mean, which status code each outcome deserves, and how JSON request/response bodies are produced and consumed.

## Syllabus deliverables
> HTTP methods, status codes, serialization and API payload processing

| Deliverable | Implemented in |
|---|---|
| ✅ HTTP methods and their semantics | `METHOD_PROPERTIES` |
| ✅ status codes | `TodoAPI.handle` |
| ✅ serialisation with an explicit encoder | `dumps` |
| ✅ deserialisation of request bodies | `Request.json` |
| ✅ payload validation and error bodies | `TodoAPI._validate` |
| ✅ response objects | `Response` |

## Key learnings
- Safe methods (GET) don't change state; idempotent ones (PUT, DELETE) can be repeated safely.
- Choose precise status codes: 201 Created, 204 No Content, 404, 405, 415, 422.
- Error responses deserve a consistent JSON body too.

## Pitfalls I hit (and how I fixed them)
- A JSON body may legally be a number or `null`; the old client rejected those.

## Run it
```bash
./propython.sh 57                 # study mode: explanation, code map, notes and tests
python -m src.day_57_rest_apis_json.main
pytest tests/test_day_57.py -v
```

## Next step
- Talk to real APIs with `requests` on Day 58.
