# Day 93 – Simple Async Network Service Reflection

**Date:** 2026-10-01 · **Level:** Capstone · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_93_async_network_service/main.py`](../../src/day_93_async_network_service/main.py) · **Tests:** [`tests/test_day_93.py`](../../tests/test_day_93.py) (7 tests)

## Scenario
A *pub-quiz game server*. Players connect over TCP with a tiny line protocol (``JOIN``, ``ANSWER``, ``SCORES``, ``QUIT``); questions are broadcast to everyone, only the first correct answer scores, and a hand-written HTTP endpoint serves the live scoreboard as JSON – all on ``asyncio`` streams from the standard library, no framework.

## Syllabus deliverables
> An asyncio TCP/HTTP server with the standard library or aiohttp, without a full framework

| Deliverable | Implemented in |
|---|---|
| ✅ TCP server with a coroutine per client | `QuizServer.handle_client` |
| ✅ line protocol commands | `QuizServer.command` |
| ✅ broadcast to all players | `QuizServer.broadcast` |
| ✅ HTTP scoreboard endpoint | `QuizServer.handle_http` |
| ✅ start both listeners | `QuizServer.start` |
| ✅ graceful shutdown | `QuizServer.close` |

## Key learnings
- `asyncio.start_server` runs one coroutine per client on a single thread.
- A line protocol with validation and broadcast needs only `readline`, `write` and `drain`.
- Timeouts, line-length limits and a goodbye on shutdown make even a small server robust.

## Pitfalls I hit (and how I fixed them)
- Forgetting `await writer.drain()` ignores back-pressure and lets buffers grow without bound.

## Run it
```bash
./propython.sh 93                 # study mode: explanation, code map, notes and tests
python -m src.day_93_async_network_service.main
pytest tests/test_day_93.py -v
```

## Next step
- Build a reusable validation library on Day 94.
