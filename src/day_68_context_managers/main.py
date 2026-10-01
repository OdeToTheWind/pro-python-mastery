"""Day 68 – Context Managers.

Scenario: a *laboratory experiment runner*. Instruments must always be
switched off, partial results rolled back on failure, and timings recorded –
even when an experiment crashes halfway.

Deliverables (syllabus):
* The ``with`` statement (setup/teardown guaranteed)
* ``__enter__`` and ``__exit__`` (including suppressing exceptions)
* ``contextlib`` (``@contextmanager``, ``ExitStack``, ``suppress``,
  ``redirect_stdout``, ``nullcontext``, ``chdir``)
"""

from __future__ import annotations

import contextlib
import io
import os
import time
from collections.abc import Callable, Iterator
from dataclasses import dataclass, field
from pathlib import Path
from types import TracebackType
from typing import Self

DELIVERABLES: dict[str, str] = {
    "class-based context manager (__enter__/__exit__)": "Instrument",
    "transaction with rollback in __exit__": "ResultsLog.transaction",
    "suppressing a specific exception": "IgnoreCalibrationWarnings",
    "@contextmanager generator": "timer",
    "ExitStack for a dynamic number of resources": "run_experiment",
    "contextlib.suppress / redirect_stdout / nullcontext / chdir": "capture_output",
}


class CalibrationWarning(Exception):
    """A recoverable instrument glitch."""


@dataclass
class Instrument:
    name: str
    events: list[str]
    fail_on_enter: bool = False
    is_on: bool = False

    def __enter__(self) -> Self:
        if self.fail_on_enter:
            raise RuntimeError(f"{self.name} failed to power on")
        self.is_on = True
        self.events.append(f"{self.name} on")
        return self  # bound to the name after `as`

    def __exit__(self, exc_type: type[BaseException] | None, exc: BaseException | None,
                 tb: TracebackType | None) -> None:
        # Returning None (falsy) means "don't swallow the error" – it propagates.
        self.is_on = False
        self.events.append(f"{self.name} off" + (f" after {exc_type.__name__}" if exc_type else ""))


class IgnoreCalibrationWarnings:
    """``__exit__`` returning True suppresses *only* the exception types it chooses."""

    def __init__(self) -> None:
        self.ignored = 0

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type: type[BaseException] | None, exc: BaseException | None,
                 tb: TracebackType | None) -> bool:
        if exc_type is not None and issubclass(exc_type, CalibrationWarning):
            self.ignored += 1
            return True
        return False


@dataclass
class ResultsLog:
    rows: list[str] = field(default_factory=list)

    @contextlib.contextmanager
    def transaction(self) -> Iterator[list[str]]:
        """Stage rows; commit on success, roll back if the block raises."""
        staged: list[str] = []
        try:
            yield staged
        except Exception:
            staged.clear()  # rollback
            raise
        else:
            self.rows.extend(staged)  # commit


@contextlib.contextmanager
def timer(label: str, results: dict[str, float], clock: Callable[[], float] = time.perf_counter) -> Iterator[None]:
    """Code before ``yield`` is __enter__, code after (in ``finally``) is __exit__."""
    start = clock()
    try:
        yield
    finally:
        results[label] = round(clock() - start, 6)


def run_experiment(names: list[str], log: ResultsLog, events: list[str], *,
                   fail_with: Exception | None = None, broken: str | None = None) -> str:
    """Power on any number of instruments with ``ExitStack``; all are switched off
    in reverse order, even if a later one fails to start or the experiment crashes."""
    timings: dict[str, float] = {}
    with contextlib.ExitStack() as stack, timer("experiment", timings):
        instruments = [stack.enter_context(Instrument(n, events, fail_on_enter=(n == broken))) for n in names]
        with log.transaction() as staged:
            for instrument in instruments:
                staged.append(f"{instrument.name}: reading ok")
            if fail_with is not None:
                raise fail_with
    return f"recorded {len(log.rows)} rows in {timings['experiment']:.4f}s"


def capture_output(func: Callable[[], None]) -> str:
    """``redirect_stdout`` captures prints – handy for testing CLI code."""
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        func()
    return buffer.getvalue()


def maybe_locked(lock: contextlib.AbstractContextManager[object] | None) -> contextlib.AbstractContextManager[object]:
    """``nullcontext`` lets callers write one ``with`` whether or not a lock is needed."""
    return lock if lock is not None else contextlib.nullcontext()


def cleanup_scratch(folder: Path) -> list[str]:
    """``chdir`` temporarily changes directory; ``suppress`` ignores a missing file."""
    with contextlib.chdir(folder):
        with contextlib.suppress(FileNotFoundError):
            os.remove("scratch.tmp")
        return sorted(os.listdir("."))


def main() -> None:
    print("Day 68 – Lab experiment runner\n")
    log, events = ResultsLog(), list[str]()
    print(run_experiment(["laser", "camera"], log, events))
    try:
        run_experiment(["laser", "spectrometer"], log, events, fail_with=RuntimeError("power cut"))
    except RuntimeError as exc:
        print("crashed:", exc, "| rows kept:", log.rows)
    print("events:", events)
    with IgnoreCalibrationWarnings() as guard:
        raise CalibrationWarning("drift 0.1%")
    print("calibration warnings ignored:", guard.ignored)
    print("captured:", capture_output(lambda: print("hello from a print")).strip())


if __name__ == "__main__":
    main()
