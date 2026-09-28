"""Tests for Day 57 – REST APIs & JSON."""

from __future__ import annotations

import json

import pytest

from src.day_57_rest_apis_json.main import (
    APIResponse,
    HTTPStatus,
    build_sample_user,
    deserialize,
    serialize,
)


def test_serialize_deserialize_roundtrip():
    original = build_sample_user(42)
    json_str = serialize(original)
    restored = deserialize(json_str)
    assert restored == original
    assert isinstance(json_str, str)
    assert '"id": 42' in json_str or '"id":42' in json_str.replace(" ", "")


def test_serialize_pretty_print():
    data = {"a": 1, "b": [2, 3]}
    pretty = serialize(data, indent=2)
    compact = serialize(data, indent=None)
    assert "\n" in pretty
    assert "\n" not in compact


def test_deserialize_bytes():
    payload = b'{"ok": true, "value": 7}'
    result = deserialize(payload)
    assert result == {"ok": True, "value": 7}


def test_api_response_success():
    resp = APIResponse(
        status_code=HTTPStatus.OK.value,
        headers={"Content-Type": "application/json"},
        body={"id": 1},
    )
    assert resp.is_success() is True
    assert resp.json() == {"id": 1}


def test_api_response_error():
    resp = APIResponse(
        status_code=HTTPStatus.NOT_FOUND.value,
        headers={},
        body={"error": "missing"},
    )
    assert resp.is_success() is False
    assert resp.json()["error"] == "missing"


def test_api_response_json_from_string_body():
    resp = APIResponse(
        status_code=200,
        headers={},
        body='{"hello": "world"}',
    )
    assert resp.json() == {"hello": "world"}


def test_api_response_json_invalid_type():
    resp = APIResponse(status_code=200, headers={}, body=123)
    with pytest.raises(TypeError):
        resp.json()


def test_build_sample_user_structure():
    user = build_sample_user()
    assert "id" in user
    assert "email" in user
    assert isinstance(user["roles"], list)
    assert "meta" in user
