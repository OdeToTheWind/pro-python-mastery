"""Tests for Day 54 – SMTP email (the SMTP server is always mocked)."""

from unittest.mock import MagicMock

import pytest

from src.day_54_sending_email.main import (
    EmailConfigError,
    SmtpConfig,
    build_report_email,
    main,
    send_email,
    validate_address,
)

ENV = {"SMTP_HOST": "smtp.test", "SMTP_PORT": "587", "SMTP_USERNAME": "bot",
       "SMTP_PASSWORD": "s3cret!", "SMTP_SENDER": "bot@test.org"}


def test_config_from_env():
    config = SmtpConfig.from_env(ENV)
    assert (config.host, config.port, config.use_ssl) == ("smtp.test", 587, False)
    assert "s3cret" not in repr(config)


def test_config_reports_missing_variables():
    with pytest.raises(EmailConfigError, match="SMTP_PASSWORD"):
        SmtpConfig.from_env({**ENV, "SMTP_PASSWORD": ""})


@pytest.mark.parametrize("bad", ["no-at-sign", "a@b", "x@y.z", "evil@x.com\nBcc: all@x.com", ""])
def test_validate_address_rejects(bad):
    with pytest.raises(ValueError):
        validate_address(bad)


def test_build_report_email_structure(tmp_path):
    attachment = tmp_path / "progress.csv"
    attachment.write_text("day,minutes\nMon,30\n", encoding="utf-8")
    msg = build_report_email("bot@test.org", ["a@test.org", "b@test.org"], "Asha",
                             {"Mon": 30, "Tue": 15}, attachment)
    assert msg["Subject"] == "Weekly study report for Asha: 45 minutes"
    assert msg["To"] == "a@test.org, b@test.org"
    assert msg.is_multipart()
    plain = msg.get_body(preferencelist=("plain",)).get_content()
    html = msg.get_body(preferencelist=("html",)).get_content()
    assert "- Mon: 30 min" in plain and "<td>Tue</td>" in html
    (att,) = list(msg.iter_attachments())
    assert att.get_filename() == "progress.csv" and att.get_content_type() == "text/csv"


def test_build_requires_recipient():
    with pytest.raises(ValueError):
        build_report_email("bot@test.org", [], "A", {})


def test_dry_run_does_not_connect():
    factory = MagicMock()
    msg = build_report_email("bot@test.org", ["a@test.org"], "A", {"Mon": 1})
    result = send_email(msg, SmtpConfig.from_env(ENV), smtp_factory=factory)
    assert result.startswith("[dry-run]")
    factory.assert_not_called()


def test_send_with_starttls():
    server = MagicMock()
    server.send_message.return_value = {}
    factory = MagicMock(return_value=MagicMock(__enter__=lambda _s: server, __exit__=lambda *a: None))
    msg = build_report_email("bot@test.org", ["a@test.org"], "A", {"Mon": 1})
    result = send_email(msg, SmtpConfig.from_env(ENV), dry_run=False, smtp_factory=factory)
    factory.assert_called_once_with("smtp.test", 587, timeout=20)
    server.starttls.assert_called_once()
    server.login.assert_called_once_with("bot", "s3cret!")
    assert result.startswith("sent <")


def test_send_with_implicit_ssl_reports_refused():
    server = MagicMock()
    server.send_message.return_value = {"a@test.org": (550, b"no")}
    factory = MagicMock(return_value=MagicMock(__enter__=lambda _s: server, __exit__=lambda *a: None))
    config = SmtpConfig.from_env({**ENV, "SMTP_PORT": "465"})
    msg = build_report_email("bot@test.org", ["a@test.org"], "A", {"Mon": 1})
    assert send_email(msg, config, dry_run=False, smtp_factory=factory) == "sent, but refused for: a@test.org"
    assert "context" in factory.call_args.kwargs
    server.starttls.assert_not_called()


def test_main_without_env(capsys, monkeypatch):
    for name in ENV:
        monkeypatch.delenv(name, raising=False)
    main()
    out = capsys.readouterr().out
    assert "[dry-run] would send" in out and "not-a-real-password" not in out
