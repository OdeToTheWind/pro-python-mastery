# Day 59 - Sending Parameters with the Request Reflection

**Date:** 2026-09-29  
**Python Version Used:** 3.12+  
**Time Spent:** 1.5 hours  
**Git Commit Hash (optional):** 

## What I Built / Key Deliverables
- Query-parameter demo (including list values) against httpbin
- Path-parameter construction (simple f-string / urljoin style)
- Custom header injection and verification
- Form-encoded POST vs JSON POST side-by-side comparison

## Core Learnings & Insights
- `params=` dict is the clean way to build query strings (requests handles encoding)
- Path parameters are just part of the URL – no special keyword
- Prefer `json=` over `data=` when the server expects application/json
- Custom headers (User-Agent, X-Request-ID, Accept) are set with a plain dict
- httpbin.org is perfect for inspecting exactly what the server received

## Challenges Faced & How I Solved Them
- Understanding that list values in `params` become repeated keys → verified with httpbin
- Choosing between form data and JSON for nested structures → JSON is almost always better

## Improvements for Next Time / Future Ideas
- Add file upload example (`files=` parameter)
- Show how to set cookies explicitly
- Build a tiny request-builder helper that merges default headers

## References / Resources Used
- https://requests.readthedocs.io/en/latest/user/quickstart/#passing-parameters-in-urls
- https://httpbin.org/
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers

## Self-Assessment
- Coverage goal met? All five demonstration functions are exercised by tests
- Typing strictness: fully typed
- Code cleanliness: clear, focused functions
- Personal rating: 9/10 – very practical day
