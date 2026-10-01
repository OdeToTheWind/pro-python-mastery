"""Tests for Day 58 – HTTP Requests (network is always mocked)."""

from datetime import timedelta
from unittest.mock import MagicMock

import pytest
import requests

from src.day_58_http_requests.main import (
    TIMEOUT,
    USER_AGENT,
    build_session,
    create_post,
    describe_response,
    get_posts,
    safe_get,
)


def fake_response(status=200, json_data=None, json_error=False):
    response = MagicMock(spec=requests.Response)
    response.status_code = status
    response.ok = status < 400
    response.reason = "OK"
    response.headers = {"Content-Type": "application/json"}
    response.elapsed = timedelta(milliseconds=123)
    response.url = "https://api.test/x"
    if json_error:
        response.json.side_effect = requests.JSONDecodeError("bad", "doc", 0)
    else:
        response.json.return_value = json_data
    if status >= 400:
        response.raise_for_status.side_effect = requests.HTTPError(response=response)
    return response


def test_build_session_headers_and_retries():
    session = build_session(retries=4)
    assert session.headers["User-Agent"] == USER_AGENT
    retry = session.get_adapter("https://x").max_retries
    assert retry.total == 4 and 503 in retry.status_forcelist


def test_get_posts_passes_params_and_timeout():
    session = MagicMock()
    session.get.return_value = fake_response(json_data=[{"id": 1}, {"id": 2}, {"id": 3}])
    assert get_posts(session, 2, base="https://api.test") == [{"id": 1}, {"id": 2}]
    session.get.assert_called_once_with("https://api.test/posts", params={"_limit": 2}, timeout=TIMEOUT)


def test_get_posts_validates():
    session = MagicMock()
    session.get.return_value = fake_response(json_data={"not": "a list"})
    with pytest.raises(ValueError):
        get_posts(session)
    with pytest.raises(ValueError):
        get_posts(session, 0)


def test_create_post_sends_json_body():
    session = MagicMock()
    session.post.return_value = fake_response(201, {"id": 101})
    assert create_post(session, "t", "b", base="https://api.test") == {"id": 101}
    assert session.post.call_args.kwargs["json"] == {"title": "t", "body": "b", "userId": 1}


def test_create_post_requires_201():
    session = MagicMock()
    session.post.return_value = fake_response(200, {"id": 1})
    with pytest.raises(ValueError, match="201"):
        create_post(session, "t", "b")


def test_describe_response():
    assert describe_response(fake_response()) == {"status": "200 OK", "ok": True, "content_type": "application/json",
                                                  "elapsed_ms": 123, "url": "https://api.test/x"}


@pytest.mark.parametrize(
    ("setup", "detail"),
    [
        ({"side_effect": requests.Timeout()}, "timed out"),
        ({"side_effect": requests.ConnectionError()}, "could not connect"),
        ({"side_effect": requests.TooManyRedirects("loop")}, "request failed: loop"),
        ({"return_value": fake_response(404)}, "HTTP error 404"),
        ({"return_value": fake_response(json_error=True)}, "response was not JSON"),
    ],
)
def test_safe_get_failure_modes(setup, detail):
    session = MagicMock()
    for attr, value in setup.items():
        setattr(session.get, attr, value)
    assert safe_get(session, "https://api.test") .detail == detail


def test_safe_get_http_error_without_response():
    session = MagicMock()
    session.get.return_value.raise_for_status.side_effect = requests.HTTPError("boom")
    assert safe_get(session, "u").detail == "HTTP error unknown"


def test_safe_get_success():
    session = MagicMock()
    session.get.return_value = fake_response(json_data={"a": 1})
    outcome = safe_get(session, "u")
    assert outcome.ok and outcome.data == {"a": 1}
