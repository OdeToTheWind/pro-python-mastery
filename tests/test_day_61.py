"""Tests for Day 61 – SMS Notification Automation."""

from __future__ import annotations

import os
from unittest.mock import patch

import pytest

from src.day_61_sms_notification_automation.main import (
    SMSMessage,
    get_twilio_credentials,
    notification_template,
    send_sms,
    send_sms_dry_run,
)


def test_get_twilio_credentials_missing(monkeypatch):
    for key in ("TWILIO_ACCOUNT_SID", "TWILIO_AUTH_TOKEN", "TWILIO_FROM_NUMBER"):
        monkeypatch.delenv(key, raising=False)
    creds = get_twilio_credentials()
    assert creds["account_sid"] is None
    assert creds["auth_token"] is None
    assert creds["from_number"] is None


def test_get_twilio_credentials_present(monkeypatch):
    monkeypatch.setenv("TWILIO_ACCOUNT_SID", "ACxxxxxxxx")
    monkeypatch.setenv("TWILIO_AUTH_TOKEN", "token123")
    monkeypatch.setenv("TWILIO_FROM_NUMBER", "+15551234567")
    creds = get_twilio_credentials()
    assert creds["account_sid"] == "ACxxxxxxxx"
    assert creds["from_number"] == "+15551234567"


def test_send_sms_dry_run():
    msg = send_sms_dry_run("+15557654321", "Hello from tests", from_="+15551234567")
    assert isinstance(msg, SMSMessage)
    assert msg.to == "+15557654321"
    assert msg.body == "Hello from tests"
    assert msg.status == "dry-run"
    assert msg.sid.startswith("SM")


def test_send_sms_force_dry_run():
    msg = send_sms("+15557654321", "Forced dry run", force_dry_run=True)
    assert msg.status == "dry-run"


def test_notification_template():
    text = notification_template("Test event", {"key": "value"})
    assert "Test event" in text
    assert "key" in text
    assert "Pro-Python" in text


def test_sms_message_dataclass():
    m = SMSMessage(to="+1", body="hi", from_="+2", sid="SMxxx", status="sent")
    assert m.to == "+1"
    assert m.status == "sent"
