"""Day 34 – Optional, Required and Default Parameters.

Scenario: a *CI job scheduler* whose ``schedule_job`` signature uses every
parameter kind Python offers, in the only order Python allows.

Deliverables (syllabus):
* Advanced parameter handling (required, optional, ``None`` sentinels, keyword-only required)
* ``*args`` and ``**kwargs``
* Ordering rules: positional-only, ``/``, standard, ``*args``, keyword-only, ``**kwargs``
"""

from __future__ import annotations

import inspect
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

DELIVERABLES: dict[str, str] = {
    "required vs optional parameters": "describe_parameters",
    "parameter ordering rules": "schedule_job",
    "*args": "schedule_job",
    "**kwargs": "schedule_job",
    "required keyword-only parameter": "schedule_job",
    "None sentinel vs mutable default": "add_label",
    "forwarding *args/**kwargs": "with_defaults",
}


@dataclass
class Job:
    name: str
    priority: int
    tags: tuple[str, ...]
    retries: int
    notify: str
    env: dict[str, str] = field(default_factory=dict)


def schedule_job(
    name: str,  # 1. positional-only, required
    priority: int = 5,  # 2. positional-only, optional
    /,
    *tags: str,  # 3. any number of extra positionals
    retries: int = 3,  # 4. keyword-only, optional
    notify: str,  # 5. keyword-only, REQUIRED (no default) – legal after *args
    **env: str,  # 6. any number of extra keywords
) -> Job:
    """Every parameter kind, in the order the grammar requires.

    Moving ``**env`` before ``*tags`` or a non-default positional after a
    default one is a ``SyntaxError`` – see ``ordering_rules_demo``.
    """
    if not 1 <= priority <= 10:
        raise ValueError("priority must be 1–10")
    if retries < 0:
        raise ValueError("retries cannot be negative")
    if "@" not in notify:
        raise ValueError("notify must be an email address")
    return Job(name, priority, tags, retries, notify, env)


def describe_parameters(func: Callable[..., Any]) -> list[tuple[str, str, bool]]:
    """(name, kind, required?) for each parameter, read via ``inspect``."""
    rows = []
    for param in inspect.signature(func).parameters.values():
        variadic = param.kind in (param.VAR_POSITIONAL, param.VAR_KEYWORD)
        required = param.default is param.empty and not variadic
        rows.append((param.name, param.kind.name, required))
    return rows


def ordering_rules_demo() -> dict[str, str]:
    """Compile illegal signatures and capture the interpreter's complaint."""
    attempts = {
        "default before required": "def f(a=1, b): pass",
        "**kwargs before *args": "def f(**kw, *a): pass",
        "two *args": "def f(*a, *b): pass",
        "legal full signature": "def f(a, b=1, /, c=2, *args, d, e=3, **kw): pass",
    }
    results = {}
    for label, source in attempts.items():
        try:
            compile(source, "<sig>", "exec")
            results[label] = "ok"
        except SyntaxError as exc:
            results[label] = f"SyntaxError: {exc.msg}"
    return results


def add_label(label: str, labels: list[str] | None = None) -> list[str]:
    """``None`` sentinel: a fresh list per call unless the caller passes one in."""
    labels = [] if labels is None else labels
    labels.append(label)
    return labels


def with_defaults(func: Callable[..., Job], **defaults: Any) -> Callable[..., Job]:
    """Wrap *func*, forwarding ``*args``/``**kwargs`` and filling in defaults."""

    def wrapper(*args: Any, **kwargs: Any) -> Job:
        return func(*args, **{**defaults, **kwargs})

    return wrapper


def main() -> None:
    print("Day 34 – CI job scheduler\n")
    job = schedule_job("nightly-tests", 8, "python", "slow", notify="dev@example.com", PYTHON="3.12")
    print(job)
    for name, kind, required in describe_parameters(schedule_job):
        print(f"  {name:<9} {kind:<22} {'required' if required else 'optional'}")
    print("\nOrdering rules:", ordering_rules_demo())
    team_job = with_defaults(schedule_job, notify="team@example.com", retries=1)
    print("Wrapped:", team_job("lint", 2, "fast"))
    print("Fresh lists:", add_label("a"), add_label("b"))


if __name__ == "__main__":
    main()
