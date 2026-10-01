"""Tests for Day 59 – Query Parameters, Headers & Payloads.

Requests are prepared offline, so we assert on the exact bytes that would be sent.
"""

import json
from unittest.mock import MagicMock

import pytest

from src.day_59_request_parameters_headers_payloads.main import (
    TIMEOUT,
    apply_form_request,
    describe,
    main,
    save_search_request,
    search_request,
    send,
    upload_cv_request,
)


def test_query_string_encoding_and_repeated_keys():
    prepared = search_request("python & data", location="São Paulo", remote=True, tags=["a", "b"], page=2)
    assert prepared.url == ("https://jobs.example.com/api/jobs?q=python+%26+data&location=S%C3%A3o+Paulo"
                            "&remote=true&tag=a&tag=b&page=2")


def test_none_and_empty_values_are_dropped():
    url = search_request("x").url
    assert "location" not in url and "tag=" not in url


def test_custom_headers():
    headers = search_request("x").headers
    assert headers["Accept"] == "application/json" and headers["X-Client"] == "day59"


def test_page_validation():
    with pytest.raises(ValueError):
        search_request("x", page=0)


def test_form_body():
    info = describe(apply_form_request(7, "Ada L", "ada@x.org"))
    assert info["content_type"] == "application/x-www-form-urlencoded"
    assert info["body"] == "name=Ada+L&email=ada%40x.org"


def test_multipart_upload():
    info = describe(upload_cv_request(7, "cv.pdf", b"%PDF"))
    assert info["content_type"].startswith("multipart/form-data; boundary=")
    assert 'filename="cv.pdf"' in info["body"] and 'name="consent"' in info["body"]


def test_json_body_and_auth_header():
    prepared = save_search_request("s", {"remote": True, "salary": {"min": 1}}, "tok")
    assert prepared.headers["Content-Type"] == "application/json"
    assert prepared.headers["Authorization"] == "Bearer tok"
    assert json.loads(prepared.body) == {"name": "s", "filters": {"remote": True, "salary": {"min": 1}}}


def test_send_uses_session_and_timeout():
    session = MagicMock()
    session.send.return_value.json.return_value = {"jobs": []}
    assert send(session, search_request("x")) == {"jobs": []}
    session.prepare_request.assert_called_once()
    assert session.send.call_args.kwargs["timeout"] == TIMEOUT
    session.send.return_value.raise_for_status.assert_called_once()


def test_main(capsys):
    main()
    out = capsys.readouterr().out
    assert "Content-Type: application/json" in out and "multipart/form-data" in out
