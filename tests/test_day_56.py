"""Tests for Day 56 – Hosting (the WSGI app is exercised in-process)."""

import json
from datetime import date
from wsgiref.util import setup_testing_defaults

import pytest

from src.day_56_pythonanywhere_hosting.main import (
    DEPLOY_STEPS,
    QUOTES,
    application,
    main,
    pythonanywhere_wsgi_file,
    quote_for,
)


def call(path="/", method="GET"):
    environ = {}
    setup_testing_defaults(environ)
    environ.update(PATH_INFO=path, REQUEST_METHOD=method)
    captured = {}

    def start_response(status, headers):
        captured["status"], captured["headers"] = status, dict(headers)

    body = b"".join(application(environ, start_response)).decode("utf-8")
    return captured["status"], captured["headers"], body


def test_home_page():
    status, headers, body = call("/")
    assert status == "200 OK"
    assert headers["Content-Type"] == "text/html; charset=utf-8"
    assert quote_for(date.today()) in body
    assert int(headers["Content-Length"]) == len(body.encode("utf-8"))


def test_app_name_from_environment(monkeypatch):
    monkeypatch.setenv("APP_NAME", "Asha's Quotes")
    assert "<h1>Asha's Quotes</h1>" in call("/")[2]


def test_json_api_and_health():
    status, headers, body = call("/api/quote")
    assert status == "200 OK" and json.loads(body)["quote"] in QUOTES
    assert json.loads(call("/health")[2]) == {"status": "ok"}


@pytest.mark.parametrize(("path", "method", "status"), [("/missing", "GET", "404 Not Found"),
                                                        ("/", "POST", "405 Method Not Allowed")])
def test_error_statuses(path, method, status):
    assert call(path, method)[0] == status


def test_quote_rotates_daily():
    assert quote_for(date(2026, 5, 1)) != quote_for(date(2026, 5, 2))


def test_pythonanywhere_wsgi_file_is_valid_python():
    source = pythonanywhere_wsgi_file("asha")
    compile(source, "wsgi.py", "exec")
    assert "path = '/home/asha/pro-python-mastery'" in source
    assert "import application" in source
    with pytest.raises(ValueError):
        pythonanywhere_wsgi_file("bad user")


def test_deploy_steps_cover_virtualenv_and_health():
    joined = " ".join(DEPLOY_STEPS)
    assert "venv" in joined and "/health" in joined


def test_main(capsys):
    main()
    assert "WSGI file for user 'asha'" in capsys.readouterr().out
