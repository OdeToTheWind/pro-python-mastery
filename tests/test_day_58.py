"""Tests for Day 58 – HTTP Requests with requests."""

from __future__ import annotations

from datetime import timedelta
from unittest.mock import MagicMock, patch

import pytest
import requests

from src.day_58_http_requests.main import (
    create_post,
    get_posts,
    inspect_response,
    safe_request,
)


@pytest.fixture
def mock_response():
    resp = MagicMock(spec=requests.Response)
    resp.status_code = 200
    resp.reason = "OK"
    resp.url = "https://jsonplaceholder.typicode.com/posts"
    resp.headers = {"Content-Type": "application/json"}
    resp.elapsed = timedelta(seconds=0.123)
    resp.encoding = "utf-8"
    resp.json.return_value = [
        {"id": 1, "title": "First post", "body": "…"},
        {"id": 2, "title": "Second post", "body": "…"},
        {"id": 3, "title": "Third post", "body": "…"},
    ]
    resp.raise_for_status = MagicMock()
    return resp


def test_get_posts_limit(mock_response):
    with patch("src.day_58_http_requests.main.requests.get", return_value=mock_response):
        posts = get_posts(limit=2)
    assert len(posts) == 2
    assert posts[0]["id"] == 1


def test_create_post(mock_response):
    mock_response.json.return_value = {
        "id": 101,
        "title": "Pro Python",
        "body": "Learning HTTP clients today",
        "userId": 1,
    }
    with patch("src.day_58_http_requests.main.requests.post", return_value=mock_response):
        created = create_post("Pro Python", "Learning HTTP clients today")
    assert created["id"] == 101
    assert created["title"] == "Pro Python"


def test_inspect_response_runs(mock_response, capsys):
    inspect_response(mock_response)
    captured = capsys.readouterr()
    assert "Status" in captured.out
    assert "200" in captured.out


def test_safe_request_success(mock_response, capsys):
    with patch("src.day_58_http_requests.main.requests.get", return_value=mock_response):
        safe_request("https://example.com")
    captured = capsys.readouterr()
    assert "Success" in captured.out


def test_safe_request_http_error(capsys):
    bad = MagicMock(spec=requests.Response)
    bad.status_code = 404
    bad.raise_for_status.side_effect = requests.HTTPError(response=bad)
    with patch("src.day_58_http_requests.main.requests.get", return_value=bad):
        safe_request("https://example.com/missing")
    captured = capsys.readouterr()
    assert "HTTP error" in captured.out


def test_safe_request_timeout(capsys):
    with patch(
        "src.day_58_http_requests.main.requests.get",
        side_effect=requests.Timeout("timed out"),
    ):
        safe_request("https://example.com/slow")
    captured = capsys.readouterr()
    assert "timed out" in captured.out.lower()
