"""Shared pytest fixtures for the 100-day test suite."""

from __future__ import annotations

from collections.abc import Callable, Iterable

import pytest


@pytest.fixture
def scripted_input(monkeypatch: pytest.MonkeyPatch) -> Callable[[Iterable[str]], list[str]]:
    """Replace ``input()`` with a scripted list of answers.

    Returns the list of prompts that were shown, so tests can assert on them.
    Raises ``EOFError`` once the script runs out, exactly like a closed stdin.
    """

    def install(answers: Iterable[str]) -> list[str]:
        queue = list(answers)
        prompts: list[str] = []

        def fake_input(prompt: str = "") -> str:
            prompts.append(prompt)
            if not queue:
                raise EOFError
            return queue.pop(0)

        monkeypatch.setattr("builtins.input", fake_input)
        return prompts

    return install
