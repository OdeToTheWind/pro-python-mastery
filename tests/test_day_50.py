"""Tests for Day 50 – Advanced Exception Handling."""

import json
import logging

import pytest

from src.day_50_error_handling_exceptions.main import (
    ConfigError,
    load_service_config,
    main,
    parse_config,
    remove_stale_lock,
    retry,
    validate_config,
)


def test_parse_config_chains_and_annotates():
    with pytest.raises(ConfigError) as info:
        parse_config('{"a": }', "svc.json")
    assert isinstance(info.value.__cause__, json.JSONDecodeError)
    assert info.value.__notes__[0].startswith("line 1, column 7")


def test_parse_config_requires_object():
    with pytest.raises(ConfigError, match="JSON object"):
        parse_config("[1, 2]")


def test_validate_config_reports_all_problems():
    with pytest.raises(ExceptionGroup) as info:
        validate_config({"service": 1, "port": 70000, "workers": True})
    kinds = sorted(type(e).__name__ for e in info.value.exceptions)
    assert kinds == ["TypeError", "TypeError", "ValueError"]


def test_validate_config_missing_keys():
    with pytest.raises(ExceptionGroup) as info:
        validate_config({})
    assert all(isinstance(e, KeyError) for e in info.value.exceptions)


def test_retry_succeeds_after_transient_failures():
    calls, waits = [], []

    def flaky():
        calls.append(1)
        if len(calls) < 3:
            raise OSError("busy")
        return "ok"

    assert retry(flaky, attempts=3, delay=0.5, sleep=waits.append) == "ok"
    assert waits == [0.5, 1.0]


def test_retry_reraises_last_error_and_ignores_other_types():
    with pytest.raises(OSError):
        retry(lambda: (_ for _ in ()).throw(OSError("down")), attempts=2, sleep=lambda _s: None)
    with pytest.raises(ValueError):
        retry(lambda: int("x"), sleep=lambda _s: None)


def test_remove_stale_lock(tmp_path):
    lock = tmp_path / "x.lock"
    remove_stale_lock(lock)  # absent: no error
    lock.write_text("1", encoding="utf-8")
    remove_stale_lock(lock)
    assert not lock.exists()


def test_load_good_config(tmp_path):
    path = tmp_path / "c.json"
    path.write_text('{"service": "api", "port": 80, "workers": 2}', encoding="utf-8")
    assert load_service_config(path) == ({"service": "api", "port": 80, "workers": 2}, [])


def test_load_groups_errors_by_type(tmp_path):
    path = tmp_path / "c.json"
    path.write_text('{"service": 1, "port": 0}', encoding="utf-8")
    config, problems = load_service_config(path)
    assert config is None
    assert problems == ["schema: 'service' must be str", "schema: missing 'workers'",
                        "value: 'port' must be 1–65535"]


def test_load_logs_parse_errors(tmp_path, caplog):
    path = tmp_path / "bad.json"
    path.write_text("{oops", encoding="utf-8")
    with caplog.at_level(logging.ERROR, logger="config"):
        _, problems = load_service_config(path)
    assert problems[0].startswith("parse: bad.json is not valid JSON (line 1")
    assert caplog.records[0].exc_info is not None


def test_load_missing_file(tmp_path):
    assert load_service_config(tmp_path / "nope.json") == (None, ["missing: nope.json"])


def test_load_retries_timeouts(tmp_path):
    attempts = []

    def slow_reader(_path):
        attempts.append(1)
        if len(attempts) == 1:
            raise TimeoutError
        return '{"service": "a", "port": 1, "workers": 1}'

    config, _ = load_service_config(tmp_path / "remote.json", read=slow_reader)
    assert config is not None and len(attempts) == 2


def test_main(capsys):
    main()
    out = capsys.readouterr().out
    assert "good.json     → {'service': 'api'" in out
    assert "missing: absent.json" in out
