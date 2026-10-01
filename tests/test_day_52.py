"""Tests for Day 52 – JSON."""

import json
from datetime import UTC, datetime
from decimal import Decimal

import pytest

from src.day_52_working_with_jsons.main import (
    SAMPLE_PAYLOAD,
    PayloadError,
    Reading,
    from_json,
    load_json,
    main,
    parse_reading,
    save_json,
    to_json,
)


def test_parse_reading():
    reading = parse_reading(SAMPLE_PAYLOAD)
    assert reading == Reading("Reykjavík-01", datetime(2026, 5, 3, 6, tzinfo=UTC), Decimal("4.1"), 87)


def test_parse_reading_accepts_bytes_and_int_temperature():
    payload = b'{"station": "a", "taken_at": "2026-01-01T00:00:00", "temperature_c": 3, "humidity": 0}'
    assert parse_reading(payload).temperature_c == Decimal("3")


@pytest.mark.parametrize(
    ("payload", "message"),
    [
        ("{bad", "invalid JSON"),
        ("[1]", "JSON object"),
        ('{"station": "a"}', "missing field 'taken_at'"),
        ('{"station": 1, "taken_at": "2026-01-01T00:00:00", "temperature_c": 1, "humidity": 1}', "'station'"),
        ('{"station": "a", "taken_at": "yesterday", "temperature_c": 1, "humidity": 1}', "'taken_at'"),
        ('{"station": "a", "taken_at": "2026-01-01T00:00:00", "temperature_c": 1, "humidity": true}', "'humidity'"),
        ('{"station": "a", "taken_at": "2026-01-01T00:00:00", "temperature_c": 1, "humidity": 101}', "0–100"),
    ],
)
def test_parse_reading_rejects(payload, message):
    with pytest.raises(PayloadError, match=message):
        parse_reading(payload)


def test_invalid_json_keeps_cause():
    with pytest.raises(PayloadError) as info:
        from_json("{")
    assert isinstance(info.value.__cause__, json.JSONDecodeError)


def test_decimal_precision_is_kept():
    assert from_json('{"x": 0.1}')["x"] == Decimal("0.1")


def test_encoder_handles_special_types():
    reading = parse_reading(SAMPLE_PAYLOAD)
    data = json.loads(to_json({"r": reading, "tags": {"b", "a"}}))
    assert data == {"r": {"station": "Reykjavík-01", "taken_at": "2026-05-03T06:00:00+00:00",
                          "temperature_c": "4.1", "humidity": 87}, "tags": ["a", "b"]}


def test_encoder_still_rejects_unknown_types():
    with pytest.raises(TypeError):
        to_json({"x": object()})


def test_pretty_vs_compact():
    assert to_json({"b": 1, "a": "é"}) == '{\n  "a": "é",\n  "b": 1\n}'
    assert to_json({"b": 1, "a": 2}, pretty=False) == '{"b":1,"a":2}'


def test_save_and_load_round_trip(tmp_path):
    path = tmp_path / "sub" / "r.json"
    save_json(path, {"at_least": 1, "taken_at": datetime(2026, 1, 1, tzinfo=UTC)})
    assert load_json(path) == {"at_least": 1, "taken_at": datetime(2026, 1, 1, tzinfo=UTC)}


def test_load_json_missing_and_corrupt(tmp_path):
    assert load_json(tmp_path / "none.json", default={}) == {}
    corrupt = tmp_path / "bad.json"
    corrupt.write_text("{oops", encoding="utf-8")
    with pytest.raises(PayloadError):
        load_json(corrupt)


def test_main(capsys):
    main()
    out = capsys.readouterr().out
    assert "Rejected: invalid JSON" in out and "humidity must be 0–100" in out
