"""Tests for Day 68 – Context Managers."""

import threading
from itertools import count

import pytest

from src.day_68_context_managers.main import (
    CalibrationWarning,
    IgnoreCalibrationWarnings,
    Instrument,
    ResultsLog,
    capture_output,
    cleanup_scratch,
    main,
    maybe_locked,
    run_experiment,
    timer,
)


def test_instrument_turns_off_even_on_error():
    events = []
    with pytest.raises(ZeroDivisionError), Instrument("laser", events) as laser:
        assert laser.is_on
        _ = 1 / 0
    assert not laser.is_on
    assert events == ["laser on", "laser off after ZeroDivisionError"]


def test_suppressing_only_selected_exceptions():
    with IgnoreCalibrationWarnings() as guard:
        raise CalibrationWarning
    assert guard.ignored == 1
    with pytest.raises(ValueError), IgnoreCalibrationWarnings():
        raise ValueError("real problem")


def test_transaction_commits_and_rolls_back():
    log = ResultsLog()
    with log.transaction() as staged:
        staged.append("a")
    with pytest.raises(RuntimeError), log.transaction() as staged:
        staged.append("b")
        raise RuntimeError
    assert log.rows == ["a"]


def test_timer_records_even_on_error():
    ticks = count(10)
    results = {}
    with pytest.raises(KeyError), timer("t", results, clock=lambda: next(ticks)):
        raise KeyError
    assert results == {"t": 1}


def test_run_experiment_success_order():
    log, events = ResultsLog(), []
    assert run_experiment(["a", "b"], log, events).startswith("recorded 2 rows")
    assert events == ["a on", "b on", "b off", "a off"]  # LIFO teardown


def test_run_experiment_rolls_back_and_powers_down():
    log, events = ResultsLog(), []
    with pytest.raises(RuntimeError):
        run_experiment(["a", "b"], log, events, fail_with=RuntimeError("cut"))
    assert log.rows == []
    assert events[-2:] == ["b off after RuntimeError", "a off after RuntimeError"]


def test_exit_stack_cleans_up_when_a_later_instrument_fails_to_start():
    log, events = ResultsLog(), []
    with pytest.raises(RuntimeError, match="b failed"):
        run_experiment(["a", "b", "c"], log, events, broken="b")
    assert events == ["a on", "a off after RuntimeError"]


def test_capture_output():
    assert capture_output(lambda: print("x")) == "x\n"


def test_maybe_locked():
    lock = threading.Lock()
    with maybe_locked(lock):
        assert lock.locked()
    with maybe_locked(None) as value:
        assert value is None


def test_cleanup_scratch(tmp_path):
    (tmp_path / "scratch.tmp").write_text("x")
    (tmp_path / "keep.txt").write_text("y")
    assert cleanup_scratch(tmp_path) == ["keep.txt"]
    assert cleanup_scratch(tmp_path) == ["keep.txt"]  # missing file is fine


def test_main(capsys):
    main()
    out = capsys.readouterr().out
    assert "calibration warnings ignored: 1" in out and "rows kept: ['laser: reading ok'" in out
