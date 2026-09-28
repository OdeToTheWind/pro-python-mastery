"""
Day 59 – Sending Parameters with the Request
Query parameters, path parameters, request headers, form data, JSON payloads.
"""

from __future__ import annotations

import sys
from typing import Any
from urllib.parse import urlencode

import requests


HTTPBIN = "https://httpbin.org"
JSONPLACEHOLDER = "https://jsonplaceholder.typicode.com"


def query_params_demo() -> dict[str, Any]:
    """Send query string parameters."""
    params = {
        "q": "python mastery",
        "page": 2,
        "limit": 10,
        "tags": ["api", "http"],          # requests will repeat the key
    }
    resp = requests.get(f"{HTTPBIN}/get", params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    print("Query string that was actually sent:")
    print(f"  {data['url']}")
    print("Args parsed by server:")
    print(f"  {data['args']}")
    return data


def path_params_demo(post_id: int = 42) -> dict[str, Any]:
    """Path parameters are just part of the URL (no special requests feature)."""
    url = f"{JSONPLACEHOLDER}/posts/{post_id}"
    resp = requests.get(url, timeout=10)
    # We expect 404 for a non-existent high id; demonstrate status handling
    print(f"Path URL: {url} → status {resp.status_code}")
    if resp.ok:
        return resp.json()
    return {"error": "not found", "status": resp.status_code}


def custom_headers_demo() -> dict[str, Any]:
    """Send custom headers (User-Agent, Accept, Authorization-style, etc.)."""
    headers = {
        "User-Agent": "ProPythonMastery/1.0 (Day 59)",
        "Accept": "application/json",
        "X-Request-ID": "day59-demo-001",
        "X-Custom-Header": "hello-from-python",
    }
    resp = requests.get(f"{HTTPBIN}/headers", headers=headers, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    print("Headers the server saw:")
    for k, v in data["headers"].items():
        if k.lower().startswith(("x-", "user-agent", "accept")):
            print(f"  {k}: {v}")
    return data


def form_data_demo() -> dict[str, Any]:
    """application/x-www-form-urlencoded payload."""
    form = {
        "username": "ada",
        "password": "analytical",
        "remember": "on",
    }
    resp = requests.post(f"{HTTPBIN}/post", data=form, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    print("Form data received by server:")
    print(f"  {data['form']}")
    print(f"Content-Type sent: {data['headers'].get('Content-Type')}")
    return data


def json_payload_demo() -> dict[str, Any]:
    """application/json payload (preferred for modern APIs)."""
    payload = {
        "title": "Day 59",
        "body": "JSON payloads are cleaner than form data for nested structures",
        "userId": 1,
        "meta": {"source": "pro-python-mastery", "version": 1},
    }
    resp = requests.post(
        f"{JSONPLACEHOLDER}/posts",
        json=payload,          # requests sets Content-Type and serializes
        timeout=10,
    )
    resp.raise_for_status()
    created = resp.json()
    print("Created resource:")
    print(f"  id={created.get('id')} title={created.get('title')}")
    return created


def main() -> None:
    print("=" * 60)
    print("Day 59 – Request Parameters, Headers & Payloads")
    print("=" * 60)

    print("\n1. Query parameters")
    query_params_demo()

    print("\n2. Path parameters")
    path_params_demo(1)
    path_params_demo(99999)

    print("\n3. Custom headers")
    custom_headers_demo()

    print("\n4. Form data (application/x-www-form-urlencoded)")
    form_data_demo()

    print("\n5. JSON payload (application/json)")
    json_payload_demo()

    print("\n✅ Day 59 complete")


if __name__ == "__main__":
    main()
    sys.exit(0)
