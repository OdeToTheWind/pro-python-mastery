# Day 58 – HTTP Requests with requests Reflection

**Date:** 2026-09-29 · **Level:** Advanced · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_58_http_requests/main.py`](../../src/day_58_http_requests/main.py) · **Tests:** [`tests/test_day_58.py`](../../tests/test_day_58.py) (9 tests)

## Scenario
A *public-holiday dashboard client* that talks to a JSON API (JSONPlaceholder / httpbin for the demo) robustly.

## Syllabus deliverables
> GET/POST requests, response handling, sessions and timeouts

| Deliverable | Implemented in |
|---|---|
| ✅ GET request | `get_posts` |
| ✅ POST request with JSON body | `create_post` |
| ✅ response handling | `describe_response` |
| ✅ sessions with retries | `build_session` |
| ✅ timeouts | `TIMEOUT` |
| ✅ error handling | `safe_get` |

## Key learnings
- Always pass a timeout; `(connect, read)` tuples control both phases.
- A `Session` reuses connections and can retry 429/5xx responses with backoff.
- Map every failure mode (timeout, connection, HTTP, bad JSON) to a clear outcome.

## Pitfalls I hit (and how I fixed them)
- `HTTPError.response` can be `None`; reading `.status_code` blindly raised `AttributeError`.

## Run it
```bash
./propython.sh 58                 # study mode: explanation, code map, notes and tests
python -m src.day_58_http_requests.main
pytest tests/test_day_58.py -v
```

## Next step
- Make concurrent requests with asyncio/aiohttp on Day 76.
