# Day 58 - Making HTTP Requests with the Requests module Reflection

**Date:** 2026-09-29  
**Python Version Used:** 3.12+  
**Time Spent:** 2 hours  
**Git Commit Hash (optional):** 

## What I Built / Key Deliverables
- GET helper that fetches and slices posts from JSONPlaceholder
- POST helper that creates a resource and returns the simulated response
- Session demo showing cookie persistence and default headers
- Robust error-handling wrapper for Timeout / HTTPError / RequestException

## Core Learnings & Insights
- `requests` is still the de-facto standard for synchronous HTTP in Python
- Always pass a `timeout=` – never leave it at the default (None)
- `raise_for_status()` turns 4xx/5xx into exceptions you can catch cleanly
- `Session` objects give connection pooling and automatic cookie handling
- Inspecting `resp.elapsed`, `resp.headers` and `resp.url` is invaluable for debugging

## Challenges Faced & How I Solved Them
- JSONPlaceholder returns 201 for POST but still echoes the body – had to check the docs
- Distinguishing network failures from HTTP error statuses → nested except clauses

## Improvements for Next Time / Future Ideas
- Add retry logic with `urllib3.util.retry.Retry` + `HTTPAdapter`
- Support streaming large responses with `stream=True` and `iter_content`
- Abstract the base URL into a small client class for reuse

## References / Resources Used
- https://requests.readthedocs.io/
- https://jsonplaceholder.typicode.com/
- https://httpbin.org/

## Self-Assessment
- Coverage goal met? Core happy-path and error paths are tested
- Typing strictness: fully typed
- Code cleanliness: readable, good separation of concerns
- Personal rating: 8.5/10 – comfortable with the library, want more advanced retry patterns later
