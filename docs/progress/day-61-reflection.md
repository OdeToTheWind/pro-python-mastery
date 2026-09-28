# Day 61 - Sending SMS with Python Reflection

**Date:** 2026-09-29  
**Python Version Used:** 3.12+  
**Time Spent:** 1.5 hours  
**Git Commit Hash (optional):** 

## What I Built / Key Deliverables
- `SMSMessage` dataclass modelling the outgoing message
- Dry-run sender that never hits the network (safe for CI)
- Real Twilio sender behind a feature flag / credential check
- Simple notification template helper

## Core Learnings & Insights
- Always provide a dry-run / mock path for external paid services
- Twilio credentials belong exclusively in environment variables
- The client pattern (instantiate once, reuse) is the same as for HTTP APIs
- Trial accounts have sending restrictions – document them
- Separating “message construction” from “transport” keeps the code testable

## Challenges Faced & How I Solved Them
- Avoiding ImportError when `twilio` is not installed → lazy import inside the real-send function
- Making the script useful even without real credentials → force_dry_run flag + clear messaging

## Improvements for Next Time / Future Ideas
- Add support for other providers (MessageBird, AWS SNS) behind a common interface
- Queue messages and retry on transient failures
- Store delivery status callbacks if the provider supports webhooks

## References / Resources Used
- https://www.twilio.com/docs/sms/quickstart/python
- https://github.com/theskumar/python-dotenv

## Self-Assessment
- Coverage goal met? Dry-run path fully tested; real path guarded
- Typing strictness: fully typed
- Code cleanliness: no secrets in source, clear separation of concerns
- Personal rating: 8.5/10 – practical and safe for learning environments
