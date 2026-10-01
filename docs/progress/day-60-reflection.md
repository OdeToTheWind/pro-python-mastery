# Day 60 – API Authentication (Client-side) Reflection

**Date:** 2026-09-29 · **Level:** Advanced · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_60_api_authentication/main.py`](../../src/day_60_api_authentication/main.py) · **Tests:** [`tests/test_day_60.py`](../../tests/test_day_60.py) (9 tests)

## Scenario
A *weather-data aggregator* that talks to three providers, each with a different authentication scheme. Secrets come from the environment (optionally a git-ignored ``.env``), are never hard-coded and never printed.

## Syllabus deliverables
> API keys, Bearer tokens, Basic Auth and environment variables

| Deliverable | Implemented in |
|---|---|
| ✅ API key in a header | `ApiKeyAuth` |
| ✅ API key in the query string | `ApiKeyAuth` |
| ✅ Bearer token | `BearerAuth` |
| ✅ Basic Auth | `basic_auth_header` |
| ✅ credentials from environment variables | `Credentials.from_env` |
| ✅ loading a .env file explicitly | `load_env_file` |
| ✅ safe secret masking | `mask_secret` |

## Key learnings
- API keys belong in headers; query-string keys end up in logs and browser history.
- Basic Auth is base64 *encoding*, not encryption – HTTPS is mandatory.
- Custom `AuthBase` classes keep auth logic out of request code.

## Pitfalls I hit (and how I fixed them)
- The old mask showed 8 of 9 characters of a short secret; at most a quarter is shown now.
- Hard-coded fallback 'secrets' were removed – missing credentials are an error.

## Run it
```bash
./propython.sh 60                 # study mode: explanation, code map, notes and tests
python -m src.day_60_api_authentication.main
pytest tests/test_day_60.py -v
```

## Next step
- Centralise secrets in the type-safe config system (Day 91).
