"""Tests for Day 61 – SMS automation (Twilio is always faked)."""

import builtins
import sys
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from src.day_61_sms_notification_automation.main import (
    DryRunSender,
    TwilioConfig,
    TwilioSender,
    compose_alert,
    main,
    make_sender,
    mask_sid,
    validate_e164,
)

ENV = {"TWILIO_ACCOUNT_SID": "AC0123456789abcdef", "TWILIO_AUTH_TOKEN": "secret-token",
       "TWILIO_FROM_NUMBER": "+1 415 555 0100"}


@pytest.mark.parametrize(("raw", "clean"), [("+1 (415) 555-0123", "+14155550123"), ("+919876543210", "+919876543210")])
def test_validate_e164(raw, clean):
    assert validate_e164(raw) == clean


@pytest.mark.parametrize("bad", ["4155550123", "+0123456789", "+12", "+1415abc0123"])
def test_validate_e164_rejects(bad):
    with pytest.raises(ValueError):
        validate_e164(bad)


def test_mask_sid():
    assert mask_sid("AC0123456789abcdef") == "AC••••••cdef"
    assert mask_sid("short") == "••••••"


def test_compose_alert_levels_and_segments():
    body, segments = compose_alert("api", 503, 120)
    assert body.startswith("[DOWN] api: HTTP 503") and segments == 1
    assert compose_alert("api", 0, 1)[0].startswith("[DOWN] api: HTTP no response")
    assert compose_alert("x" * 200, 429, 1)[1] == 2


def test_config_from_env_and_repr():
    config = TwilioConfig.from_env(ENV)
    assert config.from_number == "+14155550100"
    assert "secret-token" not in repr(config) and "0123456789" not in repr(config)
    assert TwilioConfig.from_env({}) is None


def test_make_sender_dry_run_when_unconfigured_or_forced():
    assert isinstance(make_sender({}), DryRunSender)
    assert isinstance(make_sender(ENV, force_dry_run=True), DryRunSender)


def test_make_sender_falls_back_when_twilio_missing(monkeypatch):
    real_import = builtins.__import__

    def no_twilio(name, *args, **kwargs):
        if name.startswith("twilio"):
            raise ImportError(name)
        return real_import(name, *args, **kwargs)

    monkeypatch.delitem(sys.modules, "twilio.rest", raising=False)
    monkeypatch.setattr(builtins, "__import__", no_twilio)
    with pytest.warns(UserWarning, match="twilio is not installed"):
        assert isinstance(make_sender(ENV), DryRunSender)


def test_twilio_sender_uses_client():
    client = MagicMock()
    client.messages.create.return_value = SimpleNamespace(sid="SM123", status="queued")
    sender = make_sender(ENV, client_factory=lambda sid, token: client)
    assert isinstance(sender, TwilioSender)
    result = sender.send("+14155550123", "hello")
    assert (result.status, result.reference) == ("queued", "SM123")
    client.messages.create.assert_called_once_with(to="+14155550123", from_="+14155550100", body="hello")


def test_twilio_sender_reports_api_failures():
    client = MagicMock()
    client.messages.create.side_effect = RuntimeError("21608 unverified number")
    sender = TwilioSender(TwilioConfig.from_env(ENV), lambda *_: client)
    result = sender.send("+14155550123", "x")
    assert result.status == "failed" and "unverified" in result.reference


def test_invalid_recipient_is_rejected_before_sending():
    client = MagicMock()
    sender = TwilioSender(TwilioConfig.from_env(ENV), lambda *_: client)
    with pytest.raises(ValueError):
        sender.send("not-a-number", "x")
    client.messages.create.assert_not_called()


def test_dry_run_outbox():
    sender = DryRunSender()
    assert sender.send("+14155550123", "a").reference == "DRY0001"
    assert sender.outbox == [("+14155550123", "a")]


def test_main(capsys, monkeypatch):
    monkeypatch.delenv("SEND_SMS", raising=False)
    main()
    assert "DryRunSender" in capsys.readouterr().out
