"""Side effects live at the edge so tests can replace them with a mock."""

from __future__ import annotations

from typing import Protocol


class Notifier(Protocol):
    def send(self, to: str, subject: str, body: str) -> None: ...


class OutboxNotifier:
    """Collects messages instead of e-mailing (used in the demo and dev mode)."""

    def __init__(self) -> None:
        self.outbox: list[tuple[str, str, str]] = []

    def send(self, to: str, subject: str, body: str) -> None:
        if "@" not in to:
            raise ValueError(f"cannot send to {to!r}")
        self.outbox.append((to, subject, body))
