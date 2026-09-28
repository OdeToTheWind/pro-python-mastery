"""Tests for Day 60 – API Authentication."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
import requests

from src.day_60_api_authentication.main import (
    api_key_header_demo,
    api_key_query_demo,
    basic_auth_demo,
    bearer_token_demo,
    load_credentials,
)


def _ok_response(json_data: dict) -> MagicMock:
    resp = MagicMock(spec=requests.Response)
    resp.status_code = 200
    resp.ok = True
    resp.raise_for_status = MagicMock()
    resp.json.return_value = json_data
    return resp


def test_load_credentials_defaults(monkeypatch):
    monkeypatch.delenv("DEMO_USERNAME", raising=False)
    monkeypatch.delenv("DEMO_PASSWORD", raising=False)
    monkeypatch.delenv("DEMO_BEARER_TOKEN", raising=False)
    monkeypatch.delenv("DEMO_API_KEY", raising=False)
    creds = load_credentials()
    assert "username" in creds
    assert "bearer_token" in creds
    assert creds["username"] == "user"


def test_basic_auth_demo():
    data = {"authenticated": True, "user": "user"}
    with patch(
        "src.day_60_api_authentication.main.requests.get",
        return_value=_ok_response(data),
    ):
        result = basic_auth_demo("user", "passwd")
    assert result.get("user") == "user"


def test_bearer_token_demo():
    data = {"authenticated": True, "token": "my-secret-jwt-token-12345"}
    with patch(
        "src.day_60_api_authentication.main.requests.get",
        return_value=_ok_response(data),
    ):
        result = bearer_token_demo("my-secret-jwt-token-12345")
    assert result.get("authenticated") is True


def test_api_key_header_demo():
    data = {"headers": {"X-Api-Key": "sk_test_abc123xyz"}}
    with patch(
        "src.day_60_api_authentication.main.requests.get",
        return_value=_ok_response(data),
    ):
        result = api_key_header_demo("sk_test_abc123xyz")
    assert "headers" in result


def test_api_key_query_demo():
    data = {"args": {"api_key": "sk_test_abc123xyz"}}
    with patch(
        "src.day_60_api_authentication.main.requests.get",
        return_value=_ok_response(data),
    ):
        result = api_key_query_demo("sk_test_abc123xyz")
    assert result["args"]["api_key"] == "sk_test_abc123xyz"
