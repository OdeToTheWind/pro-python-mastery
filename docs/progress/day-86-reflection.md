# Day 86 – Custom Logging & Monitoring Tool Reflection

**Date:** 2026-10-01 · **Level:** Capstone · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_86_custom_logging_monitoring/main.py`](../../src/day_86_custom_logging_monitoring/main.py) · **Tests:** [`tests/test_day_86.py`](../../tests/test_day_86.py) (9 tests)

## Scenario
A *payment-gateway monitor*. Every payment attempt is logged as one JSON object (with the request id carried by ``contextvars``), files rotate before they fill the disk, latency and error counts are kept as metrics that render in the Prometheus text format, and an alert handler pages the on-call engineer when errors spike.

## Syllabus deliverables
> Structured logging, log rotation, and basic metrics

| Deliverable | Implemented in |
|---|---|
| ✅ JSON log formatter | `JsonFormatter` |
| ✅ request-id context filter | `RequestContextFilter` |
| ✅ rotating file handler setup | `configure_logging` |
| ✅ metrics registry | `Metrics` |
| ✅ histogram percentiles | `Histogram.percentile` |
| ✅ Prometheus text exposition | `Metrics.render` |
| ✅ error-spike alert handler | `AlertHandler` |
| ✅ log analysis | `analyse_log` |

## Key learnings
- A JSON formatter turns every log record into one machine-searchable line, including `extra=` fields.
- `contextvars` carries a request id into every log line without passing it through each function.
- Counters, gauges and histogram percentiles describe behaviour; the Prometheus text format exposes them.

## Pitfalls I hit (and how I fixed them)
- Alert handlers need de-duplication – without it, one incident produces a storm of pages.

## Run it
```bash
./propython.sh 86                 # study mode: explanation, code map, notes and tests
python -m src.day_86_custom_logging_monitoring.main
pytest tests/test_day_86.py -v
```

## Next step
- Design a plugin architecture on Day 87.
