"""Day 24 – Debugging Techniques.

Scenario: a *payroll script* that ships with a real bug. We find it with print
debugging, read its traceback, set a (switchable) breakpoint, and locate the
first failing input systematically.

Deliverables (syllabus):
* Print debugging (done properly: switchable, to stderr / logging)
* Reading tracebacks
* Breakpoints (``breakpoint()`` / ``pdb``)
* Systematic bug fixing (reproduce → isolate → fix → test)
"""

from __future__ import annotations

import functools
import logging
import sys
import traceback
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import Any

DELIVERABLES: dict[str, str] = {
    "print debugging (switchable trace)": "trace_calls",
    "reading tracebacks": "summarize_traceback",
    "breakpoints": "maybe_breakpoint",
    "systematic isolation of failing input": "first_failing_input",
    "bug and its fix side by side": "net_pay_fixed",
}

log = logging.getLogger("payroll")


def net_pay_buggy(hours: Sequence[float], rate: float) -> float:
    """BUG: overtime starts after 40h, but ``range(1, len(...))`` skips day one
    and an empty week divides by zero when computing the average day."""
    total_hours = 0.0
    for day in range(1, len(hours)):  # off-by-one: should start at 0
        total_hours += hours[day]
    average_day = total_hours / len(hours)  # ZeroDivisionError for []
    log.debug("average day: %.1f h", average_day)
    overtime = max(0.0, total_hours - 40)
    return round((total_hours - overtime) * rate + overtime * rate * 1.5, 2)


def net_pay_fixed(hours: Sequence[float], rate: float) -> float:
    """Fixed version: iterate every day, guard empty weeks and negative values."""
    if rate < 0 or any(h < 0 for h in hours):
        raise ValueError("hours and rate must be non-negative")
    total_hours = sum(hours)
    overtime = max(0.0, total_hours - 40)
    return round((total_hours - overtime) * rate + overtime * rate * 1.5, 2)


def trace_calls(enabled: bool = True, stream: Any = sys.stderr) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Decorator for print-debugging: logs arguments and results when enabled.

    Prints to *stderr* (not stdout) so debug noise never mixes with real output,
    and can be switched off without deleting lines.
    """

    def decorate(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            if enabled:
                print(f"[debug] → {func.__name__}{args}{kwargs or ''}", file=stream)
            result = func(*args, **kwargs)
            if enabled:
                print(f"[debug] ← {func.__name__} = {result!r}", file=stream)
            return result

        return wrapper

    return decorate


@dataclass(frozen=True, slots=True)
class TracebackSummary:
    exception: str
    message: str
    function: str
    line: int
    code: str


def summarize_traceback(exc: BaseException) -> TracebackSummary:
    """Read a traceback the right way: the **last line** names the exception;
    the **last frame** (just above it) is where it was raised."""
    frames = traceback.extract_tb(exc.__traceback__)
    last = frames[-1]
    return TracebackSummary(type(exc).__name__, str(exc), last.name, last.lineno or 0,
                            (last.line or "").strip())


def maybe_breakpoint(enabled: bool, hook: Callable[[], None] | None = None) -> bool:
    """Pause in the debugger only when asked to.

    ``breakpoint()`` calls ``sys.breakpointhook`` (pdb by default). Setting the
    environment variable ``PYTHONBREAKPOINT=0`` disables every breakpoint.
    """
    if not enabled:
        return False
    if hook is not None:
        hook()
    else:  # pragma: no cover – interactive
        breakpoint()
    return True


def first_failing_input[T](func: Callable[[T], Any], inputs: Sequence[T]) -> tuple[int, T, str] | None:
    """Systematic isolation: run every input and report the first one that raises."""
    for index, value in enumerate(inputs):
        try:
            func(value)
        except Exception as exc:  # noqa: BLE001 – we want any failure
            return index, value, type(exc).__name__
    return None


def main() -> None:
    week = [8, 8, 8, 8, 10]
    print("Day 24 – Debugging the payroll script\n")
    print(f"buggy={net_pay_buggy(week, 20)}  fixed={net_pay_fixed(week, 20)}  (expected 860.0)")

    traced = trace_calls(stream=sys.stdout)(net_pay_fixed)
    traced([9, 9], 15)

    try:
        net_pay_buggy([], 20)
    except ZeroDivisionError as exc:
        print("Traceback summary:", summarize_traceback(exc))

    weeks: list[list[float]] = [[8, 8], [40], [], [5]]
    print("First failing week:", first_failing_input(lambda w: net_pay_buggy(w, 10), weeks))
    print("Breakpoint triggered?", maybe_breakpoint(False))


if __name__ == "__main__":
    main()
