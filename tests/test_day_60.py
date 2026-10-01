"""Tests for Day 60 – API Authentication."""

import base64

import pytest
from requests.auth import HTTPBasicAuth

from src.day_60_api_authentication import main as day60
from src.day_60_api_authentication.main import (
    ApiKeyAuth,
    BearerAuth,
    Credentials,
    MissingCredentialsError,
    authed_request,
    basic_auth_header,
    mask_secret,
)

ENV = {"DEMO_USERNAME": "ada", "DEMO_PASSWORD": "p@ss-w0rd!", "DEMO_BEARER_TOKEN": "tok_1234567890",
       "DEMO_API_KEY": "sk_live_abcdefghijkl"}


@pytest.mark.parametrize(
    ("secret", "masked"),
    [("abcdefghi", "••••••••hi"), ("abc", "••••••••"), ("sk_live_abcdefghijkl", "••••••••ijkl"), ("", "<empty>")],
)
def test_mask_secret_never_reveals_most_of_the_secret(secret, masked):
    assert mask_secret(secret) == masked


def test_basic_auth_header_matches_requests():
    header = basic_auth_header("ada", "p@ss")
    assert base64.b64decode(header.split()[1]).decode() == "ada:p@ss"
    prepared = authed_request("https://x.test", HTTPBasicAuth("ada", "p@ss"))
    assert prepared.headers["Authorization"] == header


def test_bearer_auth():
    assert authed_request("https://x.test", BearerAuth("t0k")).headers["Authorization"] == "Bearer t0k"


def test_api_key_header_and_query():
    in_header = authed_request("https://x.test/a", ApiKeyAuth("k1"))
    assert in_header.headers["X-API-Key"] == "k1" and "k1" not in in_header.url
    in_query = authed_request("https://x.test/a?x=1", ApiKeyAuth("k 2", location="query", name="api_key"))
    assert in_query.url == "https://x.test/a?x=1&api_key=k+2"


def test_credentials_from_env_and_repr_hides_secrets():
    creds = Credentials.from_env(ENV)
    assert creds.username == "ada"
    text = repr(creds)
    assert "p@ss" not in text and "tok_" not in text and "sk_live" not in text


def test_missing_credentials_have_no_hardcoded_fallback():
    with pytest.raises(MissingCredentialsError, match="DEMO_API_KEY"):
        Credentials.from_env({**ENV, "DEMO_API_KEY": ""})


def test_import_does_not_load_dotenv():
    assert "load_dotenv" not in vars(day60)


def test_load_env_file(tmp_path, monkeypatch):
    env_file = tmp_path / ".env"
    env_file.write_text("DEMO_USERNAME=from-file\n", encoding="utf-8")
    monkeypatch.delenv("DEMO_USERNAME", raising=False)
    assert day60.load_env_file(str(env_file)) is True
    import os

    assert os.environ["DEMO_USERNAME"] == "from-file"
    monkeypatch.delenv("DEMO_USERNAME")


def test_main_never_prints_full_secrets(capsys, monkeypatch):
    for key, value in ENV.items():
        monkeypatch.setenv(key, value)
    monkeypatch.setattr(day60, "load_env_file", lambda *_a, **_k: False)
    day60.main()
    out = capsys.readouterr().out
    for secret in ("p@ss-w0rd!", "tok_1234567890", "sk_live_abcdefghijkl"):
        assert secret not in out
