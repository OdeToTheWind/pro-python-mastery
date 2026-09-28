# Day 57 - REST APIs & JSON Reflection

**Date:** 2026-09-29  
**Python Version Used:** 3.12+  
**Time Spent:** 1.5 hours  
**Git Commit Hash (optional):** 

## What I Built / Key Deliverables
- `APIResponse` dataclass that models status code, headers and body
- Helper functions `serialize` / `deserialize` using the stdlib `json` module
- Round-trip demonstration (Python object → JSON string → Python object)
- Status-code helpers (`is_success`) and realistic sample payloads

## Core Learnings & Insights
- `json.dumps` / `json.loads` are the only tools you need for basic serialization
- Always decide on `ensure_ascii`, `indent` and a `default` handler for non-JSON types
- HTTP status ranges (2xx success, 4xx client error, 5xx server error) matter more than individual codes in client code
- Dataclasses + `slots=True` give clean, memory-efficient models for API payloads
- Separating “transport” concerns (status, headers) from “payload” concerns keeps code readable

## Challenges Faced & How I Solved Them
- Deciding whether `body` should be `str` or already-parsed object → solved by accepting both and providing a `.json()` method
- Making the example self-contained without a real network call → used pure in-memory objects

## Improvements for Next Time / Future Ideas
- Add `TypedDict` or Pydantic models for stricter payload validation
- Support streaming large JSON with `json.load` on file-like objects
- Write a tiny fake “router” that returns different status codes for unit tests

## References / Resources Used
- https://docs.python.org/3/library/json.html
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
- PEP 557 – Data Classes

## Self-Assessment
- Coverage goal met? Unit tests cover the core serialize/deserialize and status helpers
- Typing strictness: fully typed
- Code cleanliness: readable, DRY, follows PEP 8
- Personal rating: 9/10 – solid foundation for the HTTP days that follow
