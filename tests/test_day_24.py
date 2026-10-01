"""Tests for Day 24 – Debugging Techniques."""

import io

import pytest

from src.day_24_debugging_techniques.main import (
    first_failing_input,
    main,
    maybe_breakpoint,
    net_pay_buggy,
    net_pay_fixed,
    summarize_traceback,
    trace_calls,
)


def test_bug_reproduced_and_fixed():
    week = [8, 8, 8, 8, 10]
    assert net_pay_buggy(week, 20) == 680.0  # day one (8 h) was skipped: 34 h × 20
    assert net_pay_fixed(week, 20) == 860.0  # 40h normal + 2h overtime at 1.5×


@pytest.mark.parametrize(
    ("hours", "rate", "pay"), [([], 20, 0.0), ([40], 10, 400.0), ([50], 10, 550.0)],
)
def test_fixed_version_edge_cases(hours, rate, pay):
    assert net_pay_fixed(hours, rate) == pay


def test_fixed_version_validates():
    with pytest.raises(ValueError):
        net_pay_fixed([-1], 10)


def test_trace_calls_writes_to_stream_and_keeps_result():
    stream = io.StringIO()
    traced = trace_calls(stream=stream)(net_pay_fixed)
    assert traced([1], 10) == 10.0
    lines = stream.getvalue().splitlines()
    assert lines == ["[debug] → net_pay_fixed([1], 10)", "[debug] ← net_pay_fixed = 10.0"]
    assert traced.__name__ == "net_pay_fixed"


def test_trace_calls_disabled_is_silent():
    stream = io.StringIO()
    trace_calls(enabled=False, stream=stream)(net_pay_fixed)([1], 1)
    assert stream.getvalue() == ""


def test_summarize_traceback_points_to_raising_line():
    with pytest.raises(ZeroDivisionError) as info:
        net_pay_buggy([], 1)
    summary = summarize_traceback(info.value)
    assert summary.exception == "ZeroDivisionError"
    assert summary.function == "net_pay_buggy"
    assert summary.code == "average_day = total_hours / len(hours)  # ZeroDivisionError for []"


def test_maybe_breakpoint_uses_hook_only_when_enabled():
    calls = []
    assert maybe_breakpoint(False, lambda: calls.append(1)) is False
    assert maybe_breakpoint(True, lambda: calls.append(1)) is True
    assert calls == [1]


def test_first_failing_input():
    assert first_failing_input(lambda w: net_pay_buggy(w, 1), [[1], [2, 3], [], [4]]) == (2, [], "ZeroDivisionError")
    assert first_failing_input(lambda w: net_pay_fixed(w, 1), [[1], []]) is None


def test_main(capsys):
    main()
    out = capsys.readouterr().out
    assert "buggy=680.0  fixed=860.0" in out
    assert "First failing week: (2, [], 'ZeroDivisionError')" in out
