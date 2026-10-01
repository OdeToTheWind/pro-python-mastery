"""Day 59 – Query Parameters, Headers & Payloads.

Scenario: a *job-board search client*. The interesting part is what goes on
the wire, so every request is first built offline with
``requests.Request(...).prepare()`` – we can inspect the exact URL, headers
and body – and only then sent through a session.

Deliverables (syllabus):
* Query strings (encoding, repeated keys, ``None`` dropped)
* Custom headers
* Forms (``application/x-www-form-urlencoded`` and multipart file upload)
* JSON request bodies
"""

from __future__ import annotations

from typing import Any

import requests

DELIVERABLES: dict[str, str] = {
    "query strings": "search_request",
    "custom headers": "search_request",
    "form-encoded body": "apply_form_request",
    "multipart file upload": "upload_cv_request",
    "JSON body": "save_search_request",
    "sending a prepared request": "send",
}

API = "https://jobs.example.com/api"
TIMEOUT = (3.05, 10)


def search_request(keywords: str, *, location: str | None = None, remote: bool = False,
                   tags: list[str] | None = None, page: int = 1) -> requests.PreparedRequest:
    """GET with a query string. Lists repeat the key; ``None`` values are omitted."""
    if page < 1:
        raise ValueError("page starts at 1")
    params: dict[str, Any] = {"q": keywords, "location": location, "remote": str(remote).lower(),
                              "tag": tags or [], "page": page}
    headers = {"Accept": "application/json", "Accept-Language": "en-GB", "X-Client": "day59"}
    return requests.Request("GET", f"{API}/jobs", params=params, headers=headers).prepare()


def apply_form_request(job_id: int, name: str, email: str) -> requests.PreparedRequest:
    """Classic HTML-form style body."""
    return requests.Request("POST", f"{API}/jobs/{job_id}/apply",
                            data={"name": name, "email": email}).prepare()


def upload_cv_request(job_id: int, filename: str, content: bytes) -> requests.PreparedRequest:
    """``files=`` produces ``multipart/form-data`` with a boundary."""
    return requests.Request("POST", f"{API}/jobs/{job_id}/cv",
                            files={"cv": (filename, content, "application/pdf")},
                            data={"consent": "yes"}).prepare()


def save_search_request(name: str, filters: dict[str, Any], token: str) -> requests.PreparedRequest:
    """``json=`` serialises nested data and sets ``Content-Type: application/json``."""
    return requests.Request("POST", f"{API}/saved-searches",
                            json={"name": name, "filters": filters},
                            headers={"Authorization": f"Bearer {token}"}).prepare()


def describe(prepared: requests.PreparedRequest) -> dict[str, Any]:
    body = prepared.body
    if isinstance(body, bytes):
        body = body.decode("utf-8", errors="replace")
    return {"method": prepared.method, "url": prepared.url,
            "content_type": prepared.headers.get("Content-Type"), "body": body}


def send(session: requests.Session, prepared: requests.PreparedRequest) -> Any:
    """Merge session defaults (cookies, auth, adapters) and send with a timeout."""
    response = session.send(session.prepare_request(_as_request(prepared)), timeout=TIMEOUT)
    response.raise_for_status()
    return response.json()


def _as_request(prepared: requests.PreparedRequest) -> requests.Request:
    return requests.Request(prepared.method, prepared.url, headers=dict(prepared.headers), data=prepared.body)


def main() -> None:
    print("Day 59 – What actually goes over the wire\n")
    examples = [
        search_request("python developer", location="Berlin", remote=True, tags=["django", "aws"]),
        apply_form_request(42, "Ada Lovelace", "ada@example.com"),
        save_search_request("remote python", {"remote": True, "salary": {"min": 60000}}, "demo-token"),
        upload_cv_request(42, "cv.pdf", b"%PDF-1.7 demo"),
    ]
    for prepared in examples:
        info = describe(prepared)
        print(f"{info['method']} {info['url']}")
        print(f"   Content-Type: {info['content_type']}")
        print(f"   Body: {str(info['body'])[:90]!r}\n")


if __name__ == "__main__":
    main()
