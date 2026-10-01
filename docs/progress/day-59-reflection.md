# Day 59 – Query Parameters, Headers & Payloads Reflection

**Date:** 2026-09-29 · **Level:** Advanced · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_59_request_parameters_headers_payloads/main.py`](../../src/day_59_request_parameters_headers_payloads/main.py) · **Tests:** [`tests/test_day_59.py`](../../tests/test_day_59.py) (9 tests)

## Scenario
A *job-board search client*. The interesting part is what goes on the wire, so every request is first built offline with ``requests.Request(...).prepare()`` – we can inspect the exact URL, headers and body – and only then sent through a session.

## Syllabus deliverables
> Query strings, custom headers, forms and JSON request bodies

| Deliverable | Implemented in |
|---|---|
| ✅ query strings | `search_request` |
| ✅ custom headers | `search_request` |
| ✅ form-encoded body | `apply_form_request` |
| ✅ multipart file upload | `upload_cv_request` |
| ✅ JSON body | `save_search_request` |
| ✅ sending a prepared request | `send` |

## Key learnings
- `params=` encodes query strings (lists repeat the key, `None` is dropped).
- `data=` sends form-encoded bodies, `files=` multipart, `json=` JSON – each sets its own Content-Type.
- Preparing requests offline lets tests assert the exact bytes that would be sent.

## Pitfalls I hit (and how I fixed them)
- The old tests only checked that mocked keys existed, never what was actually sent.

## Run it
```bash
python -m src.day_59_request_parameters_headers_payloads.main
pytest tests/test_day_59.py -v
```

## Next step
- Reuse prepared-request testing when building the automation bot suite (Day 97).
