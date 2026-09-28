"""
Day 60 – APIs with Authentication
API keys, Bearer tokens, Basic Auth, secure credential handling with
environment variables and python-dotenv.
"""

from __future__ import annotations

import base64
import os
import sys
from typing import Any

import requests
from dotenv import load_dotenv

# Load .env from project root if present
load_dotenv()

HTTPBIN = "https://httpbin.org"


def basic_auth_demo(username: str, password: str) -> dict[str, Any]:
    """HTTP Basic Authentication (Authorization: Basic …)."""
    resp = requests.get(
        f"{HTTPBIN}/basic-auth/{username}/{password}",
        auth=(username, password),          # requests handles Base64 encoding
        timeout=10,
    )
    print(f"Basic Auth status: {resp.status_code}")
    if resp.ok:
        print(f"  Authenticated as: {resp.json().get('user')}")
    return resp.json() if resp.ok else {}


def bearer_token_demo(token: str) -> dict[str, Any]:
    """Bearer token (common for OAuth2 / JWT style APIs)."""
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(f"{HTTPBIN}/bearer", headers=headers, timeout=10)
    print(f"Bearer status: {resp.status_code}")
    if resp.ok:
        data = resp.json()
        print(f"  Token accepted: {data.get('authenticated')}")
        print(f"  Token value   : {data.get('token')[:20]}…")
    return resp.json() if resp.ok else {}


def api_key_header_demo(api_key: str) -> dict[str, Any]:
    """API key sent in a custom header (very common pattern)."""
    headers = {
        "X-API-Key": api_key,
        "User-Agent": "ProPythonMastery/1.0",
    }
    # httpbin does not validate the key; we just show it is transmitted
    resp = requests.get(f"{HTTPBIN}/headers", headers=headers, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    print("API key header received by server:")
    print(f"  X-Api-Key: {data['headers'].get('X-Api-Key')}")
    return data


def api_key_query_demo(api_key: str) -> dict[str, Any]:
    """API key as a query parameter (less preferred but still used)."""
    params = {"api_key": api_key}
    resp = requests.get(f"{HTTPBIN}/get", params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    print("API key query param seen by server:")
    print(f"  {data['args']}")
    return data


def load_credentials() -> dict[str, str]:
    """Load secrets from environment (never hard-code them)."""
    return {
        "username": os.getenv("DEMO_USERNAME", "user"),
        "password": os.getenv("DEMO_PASSWORD", "passwd"),
        "bearer_token": os.getenv("DEMO_BEARER_TOKEN", "my-secret-jwt-token-12345"),
        "api_key": os.getenv("DEMO_API_KEY", "sk_test_abc123xyz"),
    }


def main() -> None:
    print("=" * 60)
    print("Day 60 – API Authentication")
    print("=" * 60)

    creds = load_credentials()
    print("\nLoaded credentials from environment (or defaults):")
    for k, v in creds.items():
        masked = v[:4] + "…" + v[-4:] if len(v) > 8 else "***"
        print(f"  {k}: {masked}")

    print("\n1. Basic Authentication")
    basic_auth_demo(creds["username"], creds["password"])

    print("\n2. Bearer Token")
    bearer_token_demo(creds["bearer_token"])

    print("\n3. API Key in header")
    api_key_header_demo(creds["api_key"])

    print("\n4. API Key as query parameter")
    api_key_query_demo(creds["api_key"])

    print("\nBest practices:")
    print("• Never commit secrets – use .env + python-dotenv or a secret manager")
    print("• Prefer header-based API keys over query parameters")
    print("• Use short-lived tokens when possible")
    print("• Always call raise_for_status() or check status codes")

    print("\n✅ Day 60 complete")


if __name__ == "__main__":
    main()
    sys.exit(0)
