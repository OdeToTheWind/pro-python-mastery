"""Day 54 – Sending Email with Python and SMTP.

Scenario: a *weekly study-report mailer*. It builds a proper MIME message
(plain text + HTML + attachment), validates addresses, reads SMTP credentials
from the environment and sends with ``smtplib`` over TLS – or does a dry run.

Deliverables (syllabus):
* Automating email delivery with ``smtplib`` (STARTTLS and implicit SSL)
* Building messages with ``email.message.EmailMessage``
* Secure credential handling (environment variables, never hard-coded or logged)
"""

from __future__ import annotations

import mimetypes
import os
import re
import smtplib
import ssl
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from email.message import EmailMessage
from email.utils import formataddr, make_msgid
from pathlib import Path
from typing import Any

DELIVERABLES: dict[str, str] = {
    "smtplib delivery (STARTTLS / SSL)": "send_email",
    "building a MIME message": "build_report_email",
    "attachments": "build_report_email",
    "address validation": "validate_address",
    "credentials from environment": "SmtpConfig.from_env",
    "dry-run mode for safe testing": "send_email",
}

ADDRESS = re.compile(r"^[^@\s]+@[^@\s]+\.[a-z]{2,}$", re.IGNORECASE)


class EmailConfigError(Exception):
    pass


@dataclass(frozen=True)
class SmtpConfig:
    host: str
    port: int
    username: str
    password: str = field(repr=False)  # never printed in logs / tracebacks
    sender: str

    @property
    def use_ssl(self) -> bool:
        return self.port == 465

    @classmethod
    def from_env(cls, env: Mapping[str, str] | None = None) -> SmtpConfig:
        env = os.environ if env is None else env
        names = ["SMTP_HOST", "SMTP_PORT", "SMTP_USERNAME", "SMTP_PASSWORD", "SMTP_SENDER"]
        missing = [n for n in names if not env.get(n)]
        if missing:
            raise EmailConfigError(f"set {', '.join(missing)} in your environment or .env file")
        return cls(env["SMTP_HOST"], int(env["SMTP_PORT"]), env["SMTP_USERNAME"],
                   env["SMTP_PASSWORD"], validate_address(env["SMTP_SENDER"]))


def validate_address(address: str) -> str:
    address = address.strip()
    if not ADDRESS.match(address) or "\n" in address or "\r" in address:
        raise ValueError(f"invalid email address: {address!r}")
    return address


def build_report_email(sender: str, to: list[str], learner: str, minutes: dict[str, int],
                       attachment: Path | None = None) -> EmailMessage:
    if not to:
        raise ValueError("at least one recipient is required")
    total = sum(minutes.values())
    msg = EmailMessage()
    msg["From"] = formataddr(("Pro Python Mastery", validate_address(sender)))
    msg["To"] = ", ".join(validate_address(a) for a in to)
    msg["Subject"] = f"Weekly study report for {learner}: {total} minutes"
    msg["Message-ID"] = make_msgid(domain="pro-python-mastery.local")
    lines = "\n".join(f"- {day}: {mins} min" for day, mins in minutes.items())
    msg.set_content(f"Hi {learner},\n\nThis week you studied {total} minutes:\n{lines}\n\nKeep going!")
    rows = "".join(f"<tr><td>{day}</td><td>{mins}</td></tr>" for day, mins in minutes.items())
    msg.add_alternative(f"<h2>Great work, {learner}!</h2><table>{rows}</table>"
                        f"<p><b>Total:</b> {total} minutes</p>", subtype="html")
    if attachment is not None:
        ctype, _ = mimetypes.guess_type(attachment.name)
        maintype, subtype = (ctype or "application/octet-stream").split("/", 1)
        msg.add_attachment(attachment.read_bytes(), maintype=maintype, subtype=subtype,
                           filename=attachment.name)
    return msg


def send_email(msg: EmailMessage, config: SmtpConfig, *, dry_run: bool = True,
               smtp_factory: Callable[..., Any] | None = None) -> str:
    """Send *msg*. Dry-run (the default) only describes what would happen."""
    if dry_run:
        return f"[dry-run] would send {msg['Subject']!r} to {msg['To']} via {config.host}:{config.port}"
    context = ssl.create_default_context()  # verifies the server certificate
    if config.use_ssl:
        factory = smtp_factory or smtplib.SMTP_SSL
        server_cm = factory(config.host, config.port, context=context, timeout=20)
    else:
        factory = smtp_factory or smtplib.SMTP
        server_cm = factory(config.host, config.port, timeout=20)
    with server_cm as server:
        if not config.use_ssl:
            server.starttls(context=context)
        server.login(config.username, config.password)
        refused = server.send_message(msg)
    if refused:
        return f"sent, but refused for: {', '.join(refused)}"
    return f"sent {msg['Message-ID']}"


def main() -> None:
    print("Day 54 – Weekly report mailer\n")
    try:
        config = SmtpConfig.from_env()
        dry_run = os.environ.get("SEND_FOR_REAL") != "1"
    except EmailConfigError as exc:
        print(f"No SMTP settings ({exc}); using a dry-run demo config.")
        config = SmtpConfig("smtp.example.com", 587, "demo", "not-a-real-password", "coach@example.com")
        dry_run = True
    msg = build_report_email(config.sender, ["learner@example.com"], "Asha",
                             {"Mon": 30, "Wed": 45, "Sat": 60})
    print(msg["Subject"])
    print(send_email(msg, config, dry_run=dry_run))
    print("Config repr hides the password:", config)


if __name__ == "__main__":
    main()
