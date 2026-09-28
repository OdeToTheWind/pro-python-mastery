# Day 60 - APIs with Authentication Reflection

**Date:** 2026-09-29  
**Python Version Used:** 3.12+  
**Time Spent:** 2 hours  
**Git Commit Hash (optional):** 

## What I Built / Key Deliverables
- Basic Auth helper using `requests`’ built-in `auth=` tuple
- Bearer token helper (Authorization header)
- API-key-in-header and API-key-in-query demos
- Credential loading via `python-dotenv` + environment variables

## Core Learnings & Insights
- Never hard-code secrets – always load from environment or a secret manager
- `requests` makes Basic Auth trivial with `auth=(user, pass)`
- Bearer tokens are just a header: `Authorization: Bearer <token>`
- Header-based API keys are preferred over query-string keys (logs, caching, security)
- Masking secrets when printing is a good habit even in demo code

## Challenges Faced & How I Solved Them
- httpbin’s `/basic-auth` endpoint requires the credentials in the URL path as well – documented it clearly
- Deciding default fallback values for missing env vars so the script still runs in CI

## Improvements for Next Time / Future Ideas
- Add OAuth2 client-credentials flow (if a free provider is available)
- Show how to rotate / refresh tokens
- Integrate with `keyring` for local secret storage

## References / Resources Used
- https://requests.readthedocs.io/en/latest/user/authentication/
- https://httpbin.org/
- https://github.com/theskumar/python-dotenv

## Self-Assessment
- Coverage goal met? All four auth styles are covered; dry-run friendly
- Typing strictness: fully typed
- Code cleanliness: secrets never appear in source
- Personal rating: 9/10 – security mindset reinforced
