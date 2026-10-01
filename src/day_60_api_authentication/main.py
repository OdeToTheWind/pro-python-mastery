"""Day 60 – API Authentication (client-side).

Scenario: a *weather-data aggregator* that talks to three providers, each
with a different authentication scheme. Secrets come from the environment
(optionally a git-ignored ``.env``), are never hard-coded and never printed.

Deliverables (syllabus):
* API keys (header vs query parameter)
* Bearer tokens
* Basic Auth (and what it really sends)
* Environment variables / ``.env`` for secrets
"""

from __future__ import annotations

import base64
import os
from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Literal

import requests
from requests.auth import AuthBase, HTTPBasicAuth

DELIVERABLES: dict[str, str] = {
    "API key in a header": "ApiKeyAuth",
    "API key in the query string": "ApiKeyAuth",
    "Bearer token": "BearerAuth",
    "Basic Auth": "basic_auth_header",
    "credentials from environment variables": "Credentials.from_env",
    "loading a .env file explicitly": "load_env_file",
    "safe secret masking": "mask_secret",
}


class MissingCredentialsError(RuntimeError):
    pass


def mask_secret(secret: str, visible: int = 4) -> str:
    """Show at most the last few characters, and never more than a quarter of the secret."""
    if not secret:
        return "<empty>"
    shown = min(visible, len(secret) // 4)
    return "•" * 8 + (secret[-shown:] if shown else "")


def basic_auth_header(username: str, password: str) -> str:
    """What ``HTTPBasicAuth`` sends: base64 is *encoding*, not encryption – HTTPS only!"""
    token = base64.b64encode(f"{username}:{password}".encode()).decode("ascii")
    return f"Basic {token}"


class BearerAuth(AuthBase):
    def __init__(self, token: str) -> None:
        self.token = token

    def __call__(self, request: requests.PreparedRequest) -> requests.PreparedRequest:
        request.headers["Authorization"] = f"Bearer {self.token}"
        return request


class ApiKeyAuth(AuthBase):
    """Attach an API key as a header (preferred) or a query parameter."""

    def __init__(self, key: str, *, location: Literal["header", "query"] = "header",
                 name: str = "X-API-Key") -> None:
        self.key, self.location, self.name = key, location, name

    def __call__(self, request: requests.PreparedRequest) -> requests.PreparedRequest:
        if self.location == "header":
            request.headers[self.name] = self.key
        else:
            request.prepare_url(request.url or "", {self.name: self.key})
        return request


@dataclass(frozen=True)
class Credentials:
    username: str
    password: str = field(repr=False)
    bearer_token: str = field(repr=False)
    api_key: str = field(repr=False)

    @classmethod
    def from_env(cls, env: Mapping[str, str] | None = None) -> Credentials:
        """Read secrets from the environment. No fallbacks: missing secrets are an error."""
        env = os.environ if env is None else env
        names = {"username": "DEMO_USERNAME", "password": "DEMO_PASSWORD",
                 "bearer_token": "DEMO_BEARER_TOKEN", "api_key": "DEMO_API_KEY"}
        missing = [var for var in names.values() if not env.get(var)]
        if missing:
            raise MissingCredentialsError(f"set {', '.join(missing)} (see .env.example)")
        return cls(**{attr: env[var] for attr, var in names.items()})


def load_env_file(path: str = ".env") -> bool:
    """Load ``.env`` explicitly from ``main()`` – never as an import side effect."""
    from dotenv import load_dotenv

    return bool(load_dotenv(path, override=False))


def authed_request(url: str, auth: AuthBase) -> requests.PreparedRequest:
    return requests.Request("GET", url, auth=auth).prepare()


def main() -> None:
    print("Day 60 – API authentication\n")
    load_env_file()
    try:
        creds = Credentials.from_env()
    except MissingCredentialsError as exc:
        print(f"{exc}\nUsing throw-away demo values for the offline walkthrough.\n")
        creds = Credentials("demo-user", "demo-pass-123", "demo-token-abcdef", "demo-key-987654")
    print("Credentials:", creds)
    print("Masked key:", mask_secret(creds.api_key))
    base = "https://httpbin.org"
    examples = {
        "API key header": authed_request(f"{base}/headers", ApiKeyAuth(creds.api_key)),
        "API key query": authed_request(f"{base}/get", ApiKeyAuth(creds.api_key, location="query", name="api_key")),
        "Bearer": authed_request(f"{base}/bearer", BearerAuth(creds.bearer_token)),
        "Basic": authed_request(f"{base}/basic-auth/{creds.username}", HTTPBasicAuth(creds.username, creds.password)),
    }
    for label, prepared in examples.items():
        auth_header = str(prepared.headers.get("Authorization") or prepared.headers.get("X-API-Key") or "—")
        url = prepared.url.replace(creds.api_key, mask_secret(creds.api_key)) if prepared.url else ""
        print(f"{label:<15} {url}\n{'':<15} auth: {mask_secret(auth_header)}")
    print("\nBest practice: header keys over query keys (URLs end up in logs); HTTPS always.")


if __name__ == "__main__":
    main()
