"""
Day 61 – Sending SMS with Python
Integrating Twilio (or similar) SMS gateways, environment variables for secrets.
This module demonstrates the client pattern and falls back to a dry-run mode
when credentials are missing (safe for CI and learning).
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from typing import Any

from dotenv import load_dotenv

load_dotenv()


@dataclass(slots=True)
class SMSMessage:
    to: str
    body: str
    from_: str | None = None
    sid: str | None = None
    status: str = "queued"


def get_twilio_credentials() -> dict[str, str | None]:
    """Load Twilio credentials from environment."""
    return {
        "account_sid": os.getenv("TWILIO_ACCOUNT_SID"),
        "auth_token": os.getenv("TWILIO_AUTH_TOKEN"),
        "from_number": os.getenv("TWILIO_FROM_NUMBER"),
    }


def send_sms_dry_run(to: str, body: str, from_: str | None = None) -> SMSMessage:
    """Simulate sending an SMS (no network call)."""
    print("[DRY-RUN] Would send SMS:")
    print(f"  From : {from_ or 'TWILIO_FROM_NUMBER'}")
    print(f"  To   : {to}")
    print(f"  Body : {body[:80]}{'…' if len(body) > 80 else ''}")
    return SMSMessage(to=to, body=body, from_=from_, sid="SMdryrun000000000000000000000000", status="dry-run")


def send_sms_twilio(to: str, body: str) -> SMSMessage:
    """
    Real Twilio send.
    Requires: pip install twilio
    and the three environment variables set.
    """
    try:
        from twilio.rest import Client  # type: ignore
    except ImportError as exc:
        raise ImportError(
            "twilio package not installed. Run: pip install twilio"
        ) from exc

    creds = get_twilio_credentials()
    if not all(creds.values()):
        raise RuntimeError(
            "Missing Twilio credentials. Set TWILIO_ACCOUNT_SID, "
            "TWILIO_AUTH_TOKEN and TWILIO_FROM_NUMBER in .env"
        )

    client = Client(creds["account_sid"], creds["auth_token"])
    message = client.messages.create(
        body=body,
        from_=creds["from_number"],
        to=to,
    )
    return SMSMessage(
        to=to,
        body=body,
        from_=creds["from_number"],
        sid=message.sid,
        status=message.status,
    )


def send_sms(to: str, body: str, *, force_dry_run: bool = False) -> SMSMessage:
    """
    High-level helper: tries real Twilio, falls back to dry-run.
    """
    creds = get_twilio_credentials()
    has_creds = all(creds.values())

    if force_dry_run or not has_creds:
        return send_sms_dry_run(to, body, from_=creds.get("from_number"))
    return send_sms_twilio(to, body)


def notification_template(event: str, details: dict[str, Any]) -> str:
    """Simple template for notification bodies."""
    return (
        f"[Pro-Python] {event}\n"
        f"Details: {details}\n"
        f"— sent by Day 61 automation"
    )


def main() -> None:
    print("=" * 60)
    print("Day 61 – SMS Notification Automation")
    print("=" * 60)

    creds = get_twilio_credentials()
    print("\nCredential check:")
    for k, v in creds.items():
        status = "✓ set" if v else "✗ missing"
        print(f"  {k}: {status}")

    # Example notification
    body = notification_template(
        "API health check passed",
        {"service": "jsonplaceholder", "latency_ms": 142},
    )

    # Always safe to run – uses dry-run when credentials are absent
    msg = send_sms(
        to=os.getenv("DEMO_TO_NUMBER", "+10000000000"),
        body=body,
        force_dry_run=True,          # set False only when you have real creds
    )

    print(f"\nResult: sid={msg.sid} status={msg.status}")
    print("\nNotes:")
    print("• Never hard-code Account SID / Auth Token")
    print("• Use environment variables or a secret manager")
    print("• Prefer dry-run mode during development and CI")
    print("• Twilio trial accounts can only send to verified numbers")

    print("\n✅ Day 61 complete")


if __name__ == "__main__":
    main()
    sys.exit(0)
