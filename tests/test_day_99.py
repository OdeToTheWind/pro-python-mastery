"""Tests for Day 99 – Observability & Debugging Toolkit."""

import json
import sys
import threading

import pytest

from src.day_99_observability_debugging.main import (
    CallTracer,
    Watchpoint,
    add_context,
    crash_report,
    export_image,
    install_crash_hooks,
    main,
    redact,
    running_total,
    span,
)


def caught(func, *args, **kwargs):
    with pytest.raises(BaseException) as info:
        func(*args, **kwargs)
    return info.value


def test_redact():
    assert redact("api_token", "abc") == redact("Password", 1) == "<redacted>"
    assert redact("name", "x" * 200).endswith("…") and len(redact("name", "x" * 200)) == 80
    assert redact("count", 3) == "3"


def test_crash_report_has_frames_locals_and_notes():
    exc = caught(export_image, [1, 2], "tiff", api_token="tok-live")
    report = crash_report(exc)
    assert report["type"] == "ValueError" and report["message"] == "unsupported format 'tiff'"
    assert report["notes"] == ["while running export_image(feature='export', api_token=<redacted>)"]
    last = report["frames"][-1]
    assert last["function"] == "export_image" and last["locals"]["api_token"] == "<redacted>"
    assert last["locals"]["fmt"] == "'tiff'" and "tok-live" not in json.dumps(report)
    assert "Traceback (most recent call last)" in report["text"]


def test_chained_and_grouped_exceptions():
    def load():
        try:
            {}["profile"]
        except KeyError as err:
            raise RuntimeError("settings unreadable") from err

    report = crash_report(caught(load))
    assert report["cause"]["type"] == "KeyError" and "context" not in report

    def implicit():
        try:
            _ = 1 / 0
        except ZeroDivisionError:
            raise ValueError("bad ratio")  # noqa: B904 - implicit chaining is the point

    assert crash_report(caught(implicit))["context"]["type"] == "ZeroDivisionError"
    group = ExceptionGroup("export batch failed", [ValueError("a.png"), OSError("disk full")])
    assert [e["type"] for e in crash_report(group)["exceptions"]] == ["ValueError", "OSError"]


def test_add_context_passes_results_through():
    @add_context(step="resize")
    def double(x):
        return x * 2

    assert double(4) == 8 and double.__name__ == "double"


def test_crash_hooks_cover_main_and_worker_threads(tmp_path):
    written = []
    before = (sys.excepthook, threading.excepthook)
    uninstall = install_crash_hooks(tmp_path / "crashes", on_crash=written.append)
    try:
        exc = caught(export_image, [1], "bmp")
        sys.excepthook(type(exc), exc, exc.__traceback__)
        worker = threading.Thread(target=export_image, args=([1], "gif"), name="exporter")
        worker.start()
        worker.join()
        assert sys.excepthook(KeyboardInterrupt, KeyboardInterrupt(), None) is None
    finally:
        uninstall()
    reports = [json.loads(p.read_text()) for p in written]
    assert [r["thread"] for r in reports] == ["MainThread", "exporter"]
    assert reports[1]["message"] == "unsupported format 'gif'"
    assert (sys.excepthook, threading.excepthook) == before


def test_call_tracer_records_nested_calls_only_in_target_module():
    tracer = CallTracer(module_filter="src.day_99")
    with tracer.tracing():
        export_image([100, 250], "png", api_token="t")
        caught(export_image, [1], "raw")
    assert tracer.events[1:6] == [
        "  → export_image(pixels=[100, 250], fmt='png', api_token=<redacted>)",
        "    → apply_filter(pixels=[100, 250], gain=1.2)",
        "    ← apply_filter = [120, 255]",
        "    → brightness(pixels=[120, 255])",
        "    ← brightness = 187.5"]
    assert "    ! export_image raised ValueError" in tracer.events
    assert not any("caught" in e or "raises" in e for e in tracer.events)  # test module is not traced


def test_redact_reaches_into_kwargs():
    assert redact("kwargs", {"api_token": "x", "size": 3}) == "{'api_token': <redacted>, 'size': 3}"


def test_watchpoint_records_each_change():
    watch = Watchpoint("total", "running_total")
    assert watch.watch(running_total, [3, 0, 4]) == 7
    assert [value for _line, value in watch.changes] == [0, 3, 7]  # adding 0 is not a change
    assert all(isinstance(line, int) for line, _ in watch.changes)


def test_spans_nest_share_trace_and_record_errors():
    lines = []
    with pytest.raises(OSError), span("export", lines.append, fmt="png"):
        with span("encode", lines.append, api_key="k") as inner:
            inner["bytes"] = 42
        with span("write", lines.append):
            raise OSError("disk full")
    encode, write, export = (json.loads(line) for line in lines)
    assert encode["trace"] == write["trace"] == export["trace"] and export["parent"] is None
    assert encode["parent"] == write["parent"] == export["span"]
    assert encode["status"] == "ok" and encode["bytes"] == 42 and encode["api_key"] == "<redacted>"
    assert write["error"] == "OSError: disk full" and export["status"] == "error" and export["ms"] >= 0
    with span("next", lines.append):
        pass
    assert json.loads(lines[-1])["trace"] != export["trace"]


def test_main(capsys):
    main()
    out = capsys.readouterr().out
    assert "watch total: 12 [" in out and "tok-secret" not in out and '"name": "encode"' in out
