"""Tests for Day 59 – Request Parameters, Headers & Payloads."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
import requests

from src.day_59_request_parameters_headers_payloads.main import (
    custom_headers_demo,
    form_data_demo,
    json_payload_demo,
    path_params_demo,
    query_params_demo,
)


def _ok_response(json_data: dict) -> MagicMock:
    resp = MagicMock(spec=requests.Response)
    resp.status_code = 200
    resp.ok = True
    resp.raise_for_status = MagicMock()
    resp.json.return_value = json_data
    return resp


def test_query_params_demo():
    data = {
        "url": "https://httpbin.org/get?q=python+mastery&page=2&limit=10&tags=api&tags=http",
        "args": {"q": "python mastery", "page": "2", "limit": "10", "tags": ["api", "http"]},
    }
    with patch(
        "src.day_59_request_parameters_headers_payloads.main.requests.get",
        return_value=_ok_response(data),
    ):
        result = query_params_demo()
    assert "args" in result


def test_path_params_found():
    with patch(
        "src.day_59_request_parameters_headers_payloads.main.requests.get",
        return_value=_ok_response({"id": 1, "title": "existing"}),
    ):
        result = path_params_demo(1)
    assert result.get("id") == 1


def test_path_params_not_found():
    resp = MagicMock(spec=requests.Response)
    resp.status_code = 404
    resp.ok = False
    with patch(
        "src.day_59_request_parameters_headers_payloads.main.requests.get",
        return_value=resp,
    ):
        result = path_params_demo(99999)
    assert result["status"] == 404


def test_custom_headers_demo():
    data = {
        "headers": {
            "User-Agent": "ProPythonMastery/1.0 (Day 59)",
            "X-Request-Id": "day59-demo-001",
            "X-Custom-Header": "hello-from-python",
            "Accept": "application/json",
        }
    }
    with patch(
        "src.day_59_request_parameters_headers_payloads.main.requests.get",
        return_value=_ok_response(data),
    ):
        result = custom_headers_demo()
    assert "headers" in result


def test_form_data_demo():
    data = {
        "form": {"username": "ada", "password": "analytical", "remember": "on"},
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
    }
    with patch(
        "src.day_59_request_parameters_headers_payloads.main.requests.post",
        return_value=_ok_response(data),
    ):
        result = form_data_demo()
    assert result["form"]["username"] == "ada"


def test_json_payload_demo():
    data = {"id": 101, "title": "Day 59", "body": "…", "userId": 1}
    with patch(
        "src.day_59_request_parameters_headers_payloads.main.requests.post",
        return_value=_ok_response(data),
    ):
        result = json_payload_demo()
    assert result["id"] == 101
    assert result["title"] == "Day 59"
