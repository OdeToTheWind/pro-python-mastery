# Day 99 – Observability & Debugging Toolkit Reflection

**Date:** 2026-10-01 · **Level:** Capstone · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_99_observability_debugging/main.py`](../../src/day_99_observability_debugging/main.py) · **Tests:** [`tests/test_day_99.py`](../../tests/test_day_99.py) (10 tests)

## Scenario
The support team of a *desktop photo-editing app* gets vague bug reports ("it crashed while exporting"). This toolkit turns every crash into a structured, secret-free report (frames, locals, notes, chained causes and exception groups), installs global hooks for the main thread and worker threads, traces nested operations as timed spans, and ships two small custom debuggers: a call tracer (``sys.settrace``) and a watchpoint debugger (``bdb``) that records every change of a variable.

## Syllabus deliverables
> Advanced traceback handling, custom debuggers, and structured logs

| Deliverable | Implemented in |
|---|---|
| ✅ structured crash report | `crash_report` |
| ✅ secret redaction in locals | `redact` |
| ✅ context notes on errors | `add_context` |
| ✅ global exception hooks | `install_crash_hooks` |
| ✅ call tracer debugger | `CallTracer` |
| ✅ watchpoint debugger | `Watchpoint` |
| ✅ trace spans as structured logs | `span` |

## Key learnings
- `TracebackException`, notes, causes and exception groups turn a crash into a structured report.
- `sys.excepthook` and `threading.excepthook` catch uncaught errors in every thread.
- `sys.settrace` and `bdb.Bdb` are enough to build a call tracer and a watchpoint debugger.

## Pitfalls I hit (and how I fixed them)
- Local variables in crash reports leak secrets unless names such as `token` or `password` are redacted, even inside dicts.

## Run it
```bash
python -m src.day_99_observability_debugging.main
pytest tests/test_day_99.py -v
```

## Next step
- Ship the portfolio capstone on Day 100.
