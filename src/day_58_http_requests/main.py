"""Day 58 – HTTP Requests with ``requests``.

Scenario: a *public-holiday dashboard client* that talks to a JSON API
(JSONPlaceholder / httpbin for the demo) robustly.

Deliverables (syllabus):
* GET and POST requests
* Response handling (status, headers, JSON, errors)
* Sessions (shared headers, connection pooling, automatic retries)
* Timeouts (connect/read) and failure handling
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

DELIVERABLES: dict[str, str] = {
    "GET request": "get_posts",
    "POST request with JSON body": "create_post",
    "response handling": "describe_response",
    "sessions with retries": "build_session",
    "timeouts": "TIMEOUT",
    "error handling": "safe_get",
}

JSONPLACEHOLDER = "https://jsonplaceholder.typicode.com"
TIMEOUT = (3.05, 10)  # (connect, read) seconds – never call the network without one
USER_AGENT = "ProPythonMastery/1.0 (+https://github.com/OdeToTheWind/pro-python-mastery)"


def build_session(retries: int = 3, backoff: float = 0.5) -> requests.Session:
    """A session reuses TCP connections and retries transient failures (429/5xx)."""
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT, "Accept": "application/json"})
    retry = Retry(total=retries, backoff_factor=backoff, status_forcelist=(429, 500, 502, 503, 504),
                  allowed_methods=("GET", "HEAD", "PUT", "DELETE"), respect_retry_after_header=True)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def get_posts(session: requests.Session, limit: int = 3, base: str = JSONPLACEHOLDER) -> list[dict[str, Any]]:
    if limit < 1:
        raise ValueError("limit must be positive")
    response = session.get(f"{base}/posts", params={"_limit": limit}, timeout=TIMEOUT)
    response.raise_for_status()
    data = response.json()
    if not isinstance(data, list):
        raise ValueError("expected a JSON list of posts")
    return data[:limit]


def create_post(session: requests.Session, title: str, body: str, user_id: int = 1,
                base: str = JSONPLACEHOLDER) -> dict[str, Any]:
    """POST with ``json=`` – requests serialises the dict and sets Content-Type."""
    response = session.post(f"{base}/posts", json={"title": title, "body": body, "userId": user_id},
                            timeout=TIMEOUT)
    response.raise_for_status()
    if response.status_code != 201:
        raise ValueError(f"expected 201 Created, got {response.status_code}")
    return response.json()


def describe_response(response: requests.Response) -> dict[str, Any]:
    return {
        "status": f"{response.status_code} {response.reason}",
        "ok": response.ok,
        "content_type": response.headers.get("Content-Type", ""),
        "elapsed_ms": round(response.elapsed.total_seconds() * 1000),
        "url": response.url,
    }


@dataclass(frozen=True, slots=True)
class Outcome:
    ok: bool
    detail: str
    data: Any = None


def safe_get(session: requests.Session, url: str) -> Outcome:
    """Turn every failure mode into a readable outcome instead of a crash."""
    try:
        response = session.get(url, timeout=TIMEOUT)
        response.raise_for_status()
    except requests.Timeout:
        return Outcome(False, "timed out")
    except requests.HTTPError as exc:
        status = exc.response.status_code if exc.response is not None else "unknown"
        return Outcome(False, f"HTTP error {status}")
    except requests.ConnectionError:
        return Outcome(False, "could not connect")
    except requests.RequestException as exc:
        return Outcome(False, f"request failed: {exc}")
    try:
        return Outcome(True, f"{response.status_code} OK", response.json())
    except requests.JSONDecodeError:
        return Outcome(False, "response was not JSON")


def main() -> None:  # pragma: no cover – live network demo
    print("Day 58 – HTTP requests (live)\n")
    with build_session() as session:
        for post in get_posts(session, 2):
            print(f"  • [{post['id']}] {post['title'][:50]}")
        print("Created:", create_post(session, "Pro Python", "Learning HTTP clients"))
        print(safe_get(session, f"{JSONPLACEHOLDER}/posts/99999"))
        print(safe_get(session, "https://does-not-exist.invalid/"))


if __name__ == "__main__":  # pragma: no cover
    main()
