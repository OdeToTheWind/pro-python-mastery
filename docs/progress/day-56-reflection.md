# Day 56 – Hosting Python Code Online with PythonAnywhere Reflection

**Date:** 2026-05-07 · **Level:** Intermediate · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_56_pythonanywhere_hosting/main.py`](../../src/day_56_pythonanywhere_hosting/main.py) · **Tests:** [`tests/test_day_56.py`](../../tests/test_day_56.py) (8 tests)

## Scenario
Deploy a tiny *"Quote of the Day" web app* – a standard-library WSGI application that runs locally with ``wsgiref`` and on PythonAnywhere unchanged.

## Syllabus deliverables
> Cloud deployment basics and live app hosting

| Deliverable | Implemented in |
|---|---|
| ✅ WSGI application (the hosting contract) | `application` |
| ✅ routing and status codes | `application` |
| ✅ health check endpoint for monitoring | `application` |
| ✅ PythonAnywhere WSGI configuration file | `pythonanywhere_wsgi_file` |
| ✅ deployment checklist | `DEPLOY_STEPS` |
| ✅ local preview server | `serve_locally` |

## Key learnings
- WSGI (`application(environ, start_response)`) is the contract every Python host speaks.
- A `/health` endpoint lets uptime monitors check the deployment.
- Configuration comes from environment variables, so the same code runs locally and in the cloud.

## Pitfalls I hit (and how I fixed them)
- Paths in the PythonAnywhere WSGI file must be absolute; usernames are validated before generating it.

## Run it
```bash
python -m src.day_56_pythonanywhere_hosting.main
pytest tests/test_day_56.py -v
```

## Next step
- Build an async HTTP service without a framework on Day 93.
