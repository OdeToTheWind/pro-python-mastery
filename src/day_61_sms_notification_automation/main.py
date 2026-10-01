"""Day 61 – SMS / Notification Automation.

Scenario: a *server-monitoring alerter* that texts the on-call engineer when a
health check fails. It integrates with Twilio when credentials and the
``twilio`` package are present, and otherwise falls back to a safe dry run.

Deliverables (syllabus):
* Twilio integration (client creation, message sending, error handling)
* Secure secrets management (environment variables, masking, no fallbacks)
"""

from __future__ import annotations

import os
import re
import warnings
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from typing import Any

DELIVERABLES: dict[str, str] = {
    "Twilio client integration": "TwilioSender",
    "dry-run fallback": "DryRunSender",
    "choosing a transport safely": "make_sender",
    "secrets from environment": "TwilioConfig.from_env",
    "secret masking": "mask_sid",
    "phone number validation (E.164)": "validate_e164",
    "message composition and segment counting": "compose_alert",
}

E164 = re.compile(r"^\+[1-9]\d{7,14}$")
GSM_SEGMENT = 160


def validate_e164(number: str) -> str:
    cleaned = re.sub(r"[\s\-()]", "", number)
    if not E164.match(cleaned):
        raise ValueError(f"{number!r} is not an E.164 phone number like +14155550123")
    return cleaned


def mask_sid(value: str) -> str:
    return value[:2] + "•" * 6 + value[-4:] if len(value) > 10 else "•" * 6


def compose_alert(service: str, status: int, latency_ms: int) -> tuple[str, int]:
    """Return (body, number of SMS segments) – long texts cost more."""
    level = "DOWN" if status >= 500 or status == 0 else "DEGRADED"
    body = f"[{level}] {service}: HTTP {status or 'no response'}, {latency_ms} ms. Ack via dashboard."
    return body, max(1, -(-len(body) // GSM_SEGMENT))


@dataclass(frozen=True)
class TwilioConfig:
    account_sid: str
    auth_token: str = field(repr=False)
    from_number: str

    @classmethod
    def from_env(cls, env: Mapping[str, str] | None = None) -> TwilioConfig | None:
        """``None`` when not configured – callers then choose the dry-run sender."""
        env = os.environ if env is None else env
        values = [env.get(k, "") for k in ("TWILIO_ACCOUNT_SID", "TWILIO_AUTH_TOKEN", "TWILIO_FROM_NUMBER")]
        if not all(values):
            return None
        return cls(values[0], values[1], validate_e164(values[2]))

    def __repr__(self) -> str:
        return f"TwilioConfig(account_sid={mask_sid(self.account_sid)!r}, from_number={self.from_number!r})"


@dataclass(frozen=True, slots=True)
class SendResult:
    to: str
    status: str
    reference: str


class DryRunSender:
    def __init__(self) -> None:
        self.outbox: list[tuple[str, str]] = []

    def send(self, to: str, body: str) -> SendResult:
        self.outbox.append((validate_e164(to), body))
        return SendResult(to, "dry-run", f"DRY{len(self.outbox):04d}")


class TwilioSender:
    def __init__(self, config: TwilioConfig, client_factory: Callable[[str, str], Any]) -> None:
        self.config = config
        self.client = client_factory(config.account_sid, config.auth_token)

    def send(self, to: str, body: str) -> SendResult:
        try:
            message = self.client.messages.create(to=validate_e164(to), from_=self.config.from_number, body=body)
        except ValueError:
            raise
        except Exception as exc:  # TwilioRestException, network errors …
            return SendResult(to, "failed", f"{type(exc).__name__}: {exc}")
        return SendResult(to, str(message.status), str(message.sid))


def make_sender(env: Mapping[str, str] | None = None, *, force_dry_run: bool = False,
                client_factory: Callable[[str, str], Any] | None = None) -> DryRunSender | TwilioSender:
    """Use Twilio only when explicitly configured *and* installed; otherwise dry-run."""
    config = None if force_dry_run else TwilioConfig.from_env(env)
    if config is None:
        return DryRunSender()
    if client_factory is None:
        try:
            from twilio.rest import Client  # optional dependency
        except ImportError:
            warnings.warn("twilio is not installed (pip install twilio); using dry-run", stacklevel=2)
            return DryRunSender()
        client_factory = Client
    return TwilioSender(config, client_factory)


def main() -> None:
    print("Day 61 – On-call SMS alerter\n")
    sender = make_sender(force_dry_run=os.environ.get("SEND_SMS") != "1")
    body, segments = compose_alert("checkout-api", 503, 2400)
    to = os.environ.get("DEMO_TO_NUMBER") or "+14155550123"
    result = sender.send(to, body)
    print(f"{type(sender).__name__}: {result}")
    print(f"Body ({segments} segment): {body}")


if __name__ == "__main__":
    main()
