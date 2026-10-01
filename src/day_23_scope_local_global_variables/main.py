"""Day 23 – Scope and Local/Global Variables.

Scenario: a *web-app feature-flag service*. Configuration lives at module
level, request handlers have their own locals and rate limiters are closures.

Deliverables (syllabus):
* The LEGB rule (Local → Enclosing → Global → Built-in)
* ``global`` and ``nonlocal`` usage
* Good scoping practices (and the ``UnboundLocalError`` trap)
"""

from __future__ import annotations

import builtins
from collections.abc import Callable
from dataclasses import dataclass, field

DELIVERABLES: dict[str, str] = {
    "LEGB lookup order": "legb_trace",
    "global keyword": "set_environment",
    "nonlocal keyword": "make_rate_limiter",
    "UnboundLocalError pitfall": "unbound_local_demo",
    "closures and captured cells": "closure_cells",
    "good practice: explicit state instead of globals": "FeatureFlags",
}

# G – module (global) scope
ENVIRONMENT = "production"
source = "global"


def legb_trace() -> dict[str, str]:
    """Resolve the name ``source`` at each level and show where each lookup lands."""
    results: dict[str, str] = {}

    def enclosing() -> None:
        source = "enclosing"  # E – enclosing function scope

        def local() -> None:
            source = "local"  # L – local scope wins first
            results["inside local()"] = source

        def no_local() -> None:
            results["inside no_local()"] = source  # falls back to E

        local()
        no_local()

    enclosing()
    results["module level"] = globals()["source"]  # G
    results["len is built-in"] = "builtins" if len is builtins.len else "shadowed"  # B
    return results


def set_environment(name: str) -> str:
    """Rebind the module-level ``ENVIRONMENT`` – requires ``global``."""
    global ENVIRONMENT
    previous, ENVIRONMENT = ENVIRONMENT, name
    return previous


def current_environment() -> str:
    return ENVIRONMENT  # reading a global needs no keyword


def unbound_local_demo() -> str:
    """Assigning anywhere in a function makes the name local for the *whole* body."""
    counter = 0

    def broken() -> int:
        counter += 1  # type: ignore[misc]  # noqa: F823 – deliberate: read-before-assign
        return counter

    try:
        broken()
    except UnboundLocalError as exc:
        return type(exc).__name__
    return "no error"


def make_rate_limiter(max_calls: int) -> Callable[[], bool]:
    """Allow *max_calls* requests; ``nonlocal`` updates the enclosing counter."""
    calls = 0

    def allow() -> bool:
        nonlocal calls
        if calls >= max_calls:
            return False
        calls += 1
        return True

    return allow


def closure_cells(func: Callable[..., object]) -> dict[str, object]:
    """Show the variables a closure has captured (``__closure__`` cells)."""
    names = func.__code__.co_freevars
    cells = func.__closure__ or ()
    return {name: cell.cell_contents for name, cell in zip(names, cells, strict=True)}


@dataclass
class FeatureFlags:
    """Preferred design: pass state explicitly instead of mutating globals."""

    flags: dict[str, bool] = field(default_factory=dict)

    def enable(self, name: str) -> None:
        self.flags[name] = True

    def is_enabled(self, name: str) -> bool:
        return self.flags.get(name, False)


def main() -> None:
    print("Day 23 – Scope & LEGB\n")
    for where, value in legb_trace().items():
        print(f"  {where:<18} → {value}")
    old = set_environment("staging")
    print(f"\nENVIRONMENT: {old} → {current_environment()}")
    set_environment(old)
    print("Read-before-assign raises:", unbound_local_demo())
    limiter = make_rate_limiter(2)
    print("Rate limiter:", [limiter() for _ in range(3)], "cells:", closure_cells(limiter))
    flags = FeatureFlags()
    flags.enable("dark_mode")
    print("Feature flags object:", flags)


if __name__ == "__main__":
    main()
