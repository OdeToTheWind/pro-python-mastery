"""
Day 57 – REST APIs & JSON
Understanding HTTP methods, status codes, JSON serialization/deserialization
with the standard library `json` module (no external HTTP library yet).
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass, asdict
from enum import Enum
from typing import Any


class HTTPMethod(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


class HTTPStatus(Enum):
    OK = 200
    CREATED = 201
    NO_CONTENT = 204
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    INTERNAL_SERVER_ERROR = 500


@dataclass(slots=True)
class APIResponse:
    """Simple in-memory representation of an API response."""

    status_code: int
    headers: dict[str, str]
    body: Any

    def is_success(self) -> bool:
        return 200 <= self.status_code < 300

    def json(self) -> Any:
        """Return body already parsed (or parse if it is still a string)."""
        if isinstance(self.body, (dict, list)):
            return self.body
        if isinstance(self.body, str):
            return json.loads(self.body)
        raise TypeError(f"Cannot parse body of type {type(self.body)}")


def serialize(data: Any, *, indent: int | None = 2, ensure_ascii: bool = False) -> str:
    """Serialize Python object → JSON string (pretty by default)."""
    return json.dumps(data, indent=indent, ensure_ascii=ensure_ascii, default=str)


def deserialize(payload: str | bytes) -> Any:
    """Deserialize JSON string/bytes → Python object."""
    if isinstance(payload, bytes):
        payload = payload.decode("utf-8")
    return json.loads(payload)


def build_sample_user(user_id: int = 1) -> dict[str, Any]:
    """Factory that returns a realistic user payload."""
    return {
        "id": user_id,
        "name": "Ada Lovelace",
        "email": "ada@analytical.engine",
        "roles": ["admin", "developer"],
        "active": True,
        "meta": {
            "created_at": "2026-01-15T10:30:00Z",
            "last_login": None,
        },
    }


def demonstrate_roundtrip() -> None:
    """Show full serialize → deserialize cycle and status handling."""
    original = build_sample_user()
    print("Original Python object:")
    print(original)
    print()

    json_str = serialize(original)
    print("Serialized JSON:")
    print(json_str)
    print()

    restored = deserialize(json_str)
    print("Restored Python object:")
    print(restored)
    print()

    assert restored == original, "Round-trip failed!"
    print("✅ Round-trip serialization successful")

    # Simulate different response statuses
    success = APIResponse(
        status_code=HTTPStatus.OK.value,
        headers={"Content-Type": "application/json"},
        body=restored,
    )
    not_found = APIResponse(
        status_code=HTTPStatus.NOT_FOUND.value,
        headers={"Content-Type": "application/json"},
        body={"error": "User not found", "code": "USER_404"},
    )

    print(f"\nSuccess response is_success? → {success.is_success()}")
    print(f"Not-found response is_success? → {not_found.is_success()}")
    print(f"Error body: {not_found.json()}")


def main() -> None:
    print("=" * 60)
    print("Day 57 – REST APIs & JSON")
    print("=" * 60)
    demonstrate_roundtrip()
    print("\nKey takeaways:")
    print("• json.dumps / json.loads are the core tools")
    print("• Always handle non-JSON bodies and status codes explicitly")
    print("• Prefer dataclasses or TypedDict for structured payloads")


if __name__ == "__main__":
    main()
    sys.exit(0)
