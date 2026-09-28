"""
Day 58 – Making HTTP Requests with the Requests module
GET/POST, response handling, status codes, timeouts, sessions.
"""

from __future__ import annotations

import sys
from typing import Any

import requests
from requests.exceptions import HTTPError, RequestException, Timeout


# Public free test APIs (no key required)
JSONPLACEHOLDER = "https://jsonplaceholder.typicode.com"
HTTPBIN = "https://httpbin.org"


def get_posts(limit: int = 3) -> list[dict[str, Any]]:
    """Fetch a few posts from JSONPlaceholder."""
    url = f"{JSONPLACEHOLDER}/posts"
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    return data[:limit]


def create_post(title: str, body: str, user_id: int = 1) -> dict[str, Any]:
    """Create a new post (JSONPlaceholder simulates creation)."""
    url = f"{JSONPLACEHOLDER}/posts"
    payload = {"title": title, "body": body, "userId": user_id}
    resp = requests.post(url, json=payload, timeout=10)
    resp.raise_for_status()
    return resp.json()


def inspect_response(resp: requests.Response) -> None:
    """Print useful metadata about a response."""
    print(f"  Status : {resp.status_code} {resp.reason}")
    print(f"  URL    : {resp.url}")
    print(f"  Headers: Content-Type={resp.headers.get('Content-Type')}")
    print(f"  Elapsed: {resp.elapsed.total_seconds():.3f}s")
    if resp.encoding:
        print(f"  Encoding: {resp.encoding}")


def session_demo() -> None:
    """Demonstrate a persistent Session (cookies, connection pooling)."""
    with requests.Session() as session:
        session.headers.update({"User-Agent": "ProPythonMastery/1.0"})
        # First request
        r1 = session.get(f"{HTTPBIN}/cookies/set/session_id/abc123", timeout=10)
        print("Set cookie response:")
        inspect_response(r1)
        # Second request automatically sends the cookie
        r2 = session.get(f"{HTTPBIN}/cookies", timeout=10)
        print("Cookies received by server:")
        print(f"  {r2.json()}")


def safe_request(url: str) -> None:
    """Show proper error handling patterns."""
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        print(f"Success: {resp.status_code}")
    except Timeout:
        print("Request timed out")
    except HTTPError as exc:
        print(f"HTTP error: {exc.response.status_code} – {exc}")
    except RequestException as exc:
        print(f"Request failed: {exc}")


def main() -> None:
    print("=" * 60)
    print("Day 58 – HTTP Requests with `requests`")
    print("=" * 60)

    print("\n1. GET posts")
    posts = get_posts(2)
    for p in posts:
        print(f"  • [{p['id']}] {p['title'][:50]}…")

    print("\n2. POST a new post")
    created = create_post("Pro Python", "Learning HTTP clients today")
    print(f"  Created id={created.get('id')} title={created.get('title')}")

    print("\n3. Session demo")
    session_demo()

    print("\n4. Error handling examples")
    safe_request(f"{JSONPLACEHOLDER}/posts/1")          # should succeed
    safe_request(f"{JSONPLACEHOLDER}/posts/99999")      # 404
    safe_request("https://httpbin.org/delay/10")         # timeout

    print("\n✅ Day 58 complete")


if __name__ == "__main__":
    main()
    sys.exit(0)
