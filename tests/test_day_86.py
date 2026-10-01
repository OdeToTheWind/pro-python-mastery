"""Tests for Day 86 – Custom Logging & Monitoring."""

import json
import logging

import pytest

from src.day_86_custom_logging_monitoring.main import (
    AlertHandler,
    Histogram,
    JsonFormatter,
    Metrics,
    RequestContextFilter,
    analyse_log,
    configure_logging,
    main,
    process_payment,
    request_context,
)


@pytest.fixture
def setup(tmp_path):
    pages = []
    logger = configure_logging(tmp_path / "payments.log", max_bytes=600, backups=2,
                               alert=AlertHandler(pages.append, threshold=2))
    yield logger, tmp_path, pages
    for handler in logger.handlers:
        handler.close()
    logger.handlers = []


def record(msg="hello", **extra):
    rec = logging.makeLogRecord({"name": "t", "levelname": "INFO", "levelno": 20, "msg": msg, **extra})
    RequestContextFilter().filter(rec)
    return rec


def test_json_formatter_includes_extras_and_context():
    with request_context("req-42"):
        line = JsonFormatter().format(record("paid %s", args=("ok",), amount_cents=500))
    data = json.loads(line)
    assert data["msg"] == "paid ok" and data["amount_cents"] == 500 and data["request_id"] == "req-42"
    assert data["ts"].endswith("+00:00")


def test_context_resets_and_newlines_stay_on_one_line():
    with request_context("outer"), request_context("inner"):
        pass
    line = JsonFormatter().format(record("line1\nline2"))
    assert "\n" not in line and json.loads(line)["request_id"] == "-"


def test_exceptions_are_serialised():
    try:
        raise ValueError("card expired")
    except ValueError:
        import sys

        rec = record(exc_info=sys.exc_info())
    assert "ValueError: card expired" in json.loads(JsonFormatter().format(rec))["exc"]


def test_rotation_keeps_limited_backups(setup):
    logger, tmp_path, _ = setup
    for n in range(40):
        with request_context(f"r{n}"):
            logger.info("payment approved", extra={"n": n})
    names = sorted(p.name for p in tmp_path.iterdir())
    assert names == ["payments.log", "payments.log.1", "payments.log.2"]
    assert all(p.stat().st_size <= 600 for p in tmp_path.iterdir())


def test_alert_fires_once_per_spike_and_rearms():
    pages, now = [], [0.0]
    handler = AlertHandler(pages.append, threshold=3, window=10, clock=lambda: now[0])
    for t in (0, 1, 2, 3):  # 4 errors, one page
        now[0] = t
        handler.emit(record("boom"))
    now[0] = 30
    handler.emit(record("late"))  # window cleared → re-armed
    for t in (31, 32):
        now[0] = t
        handler.emit(record("again"))
    assert len(pages) == 2 and pages[0].startswith("3 errors in 10s")


def test_histogram_percentiles_and_buckets():
    hist = Histogram(buckets=(0.1, 0.5))
    for v in (0.05, 0.2, 0.3, 0.4, 0.9):
        hist.observe(v)
    assert hist.percentile(50) == 0.3 and hist.percentile(100) == 0.9 and hist.percentile(1) == 0.05
    assert hist.bucket_counts() == [("0.1", 1), ("0.5", 4), ("+Inf", 5)]
    assert Histogram().percentile(99) == 0.0


def test_metrics_render_prometheus_text(setup):
    logger, _, pages = setup
    metrics = Metrics()
    assert process_payment(logger, metrics, 500, latency=0.1)
    assert not process_payment(logger, metrics, 500, latency=0.2, declined=True)
    process_payment(logger, metrics, 0, latency=0.3)
    process_payment(logger, metrics, -1, latency=0.3)
    metrics.set_gauge("gateway_up", 1)
    text = metrics.render()
    assert 'payments_total{status="approved"} 1' in text and 'payments_total{status="error"} 2' in text
    assert 'payment_latency_seconds_bucket{le="+Inf"} 4' in text and "gateway_up 1" in text
    assert "payment_latency_seconds_sum 0.900" in text and len(pages) == 1


def test_analyse_log_reads_rotated_files(setup):
    logger, tmp_path, _ = setup
    metrics = Metrics()
    for n in range(12):
        with request_context(f"r{n % 4}"):
            process_payment(logger, metrics, 0 if n % 3 == 0 else 100, latency=0.01)
    summary = analyse_log(tmp_path)
    assert summary["files"] >= 2 and summary["lines"] <= 12 and summary["requests"] <= 4
    assert summary["levels"]["ERROR"] / summary["lines"] == pytest.approx(summary["error_rate"], abs=0.001)
    assert analyse_log(tmp_path / "nothing")["error_rate"] == 0.0


def test_main(capsys):
    main()
    out = capsys.readouterr().out
    assert "p95 latency:" in out and "pages: ['3 errors" in out
