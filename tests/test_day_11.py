"""Tests for Day 11 – Error Handling."""

import pytest

from src.day_11_error_handling.main import (
    ask_float,
    average,
    load_readings,
    main,
    parse_line,
    provoke,
)


def test_parse_line_ok():
    assert parse_line(" north , 21.5\n") == ("north", 21.5)


@pytest.mark.parametrize("line", ["north", "north,abc", ",20", "a,b,c"])
def test_parse_line_errors(line):
    with pytest.raises(ValueError):
        parse_line(line)


def test_load_readings_records_every_block(tmp_path):
    log = tmp_path / "s.log"
    log.write_text("a,1\nb,oops\n\nc,3\n", encoding="utf-8")
    report = load_readings(log)
    assert report.readings == {"a": 1.0, "c": 3.0}
    assert report.skipped == ["line 2: could not convert string to float: 'oops'"]
    assert report.events == ["else: file opened", "finally: file closed"]


def test_load_readings_missing_file(tmp_path):
    report = load_readings(tmp_path / "absent.log")
    assert report.events == ["except: file missing"]
    assert report.readings == {}


def test_average_handles_empty():
    assert average({}) is None
    assert average({"a": 1, "b": 3}) == 2


@pytest.mark.parametrize(
    "kind",
    ["ValueError", "TypeError", "ZeroDivisionError", "IndexError", "KeyError",
     "AttributeError", "FileNotFoundError"],
)
def test_provoke_common_exceptions(kind):
    assert provoke(kind) == kind


def test_provoke_unknown():
    with pytest.raises(ValueError):
        provoke("MemoryError")


def _answers(*values):
    queue = list(values)

    def fake(_prompt):
        if not queue:
            raise EOFError
        return queue.pop(0)

    return fake


def test_ask_float_retries(capsys):
    assert ask_float("t: ", _answers("x", "20.5")) == 20.5
    assert "please type a number" in capsys.readouterr().out


def test_ask_float_gives_up():
    assert ask_float("t: ", _answers("a", "b", "c")) is None
    assert ask_float("t: ", _answers()) is None


def test_main(capsys, scripted_input):
    scripted_input(["18.25"])
    main()
    out = capsys.readouterr().out
    assert "west = 18.25" in out
    assert "finally: file closed" in out
