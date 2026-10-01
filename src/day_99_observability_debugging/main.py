"""Day 99 – Capstone: Observability & Debugging Toolkit.

Scenario: the support team of a *desktop photo-editing app* gets vague bug
reports ("it crashed while exporting"). This toolkit turns every crash into a
structured, secret-free report (frames, locals, notes, chained causes and
exception groups), installs global hooks for the main thread and worker
threads, traces nested operations as timed spans, and ships two small custom
debuggers: a call tracer (``sys.settrace``) and a watchpoint debugger
(``bdb``) that records every change of a variable.

Deliverables (syllabus):
* Advanced traceback handling (``TracebackException``, locals, notes,
  ``__cause__``, ``ExceptionGroup``), redaction of secrets
* Global crash hooks (``sys.excepthook``, ``threading.excepthook``)
* Custom debuggers (``sys.settrace`` call tracer, ``bdb.Bdb`` watchpoints)
* Structured logs with trace/span ids and durations
"""

from __future__ import annotations

import bdb
import contextvars
import functools
import itertools
import json
import re
import sys
import threading
import time
import traceback
from collections.abc import Callable, Iterator, Mapping
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path
from types import FrameType, TracebackType
from typing import Any, ParamSpec, TypeVar, cast

DELIVERABLES: dict[str, str] = {
    "structured crash report": "crash_report",
    "secret redaction in locals": "redact",
    "context notes on errors": "add_context",
    "global exception hooks": "install_crash_hooks",
    "call tracer debugger": "CallTracer",
    "watchpoint debugger": "Watchpoint",
    "trace spans as structured logs": "span",
}

P = ParamSpec("P")
R = TypeVar("R")
SECRET_NAME = re.compile(r"pass(word)?|secret|token|api_?key|auth", re.IGNORECASE)


def redact(name: str, value: Any, limit: int = 80) -> str:
    """Hide values whose *name* looks secret – also inside dicts such as ``**kwargs``."""
    if SECRET_NAME.search(name):
        return "<redacted>"
    if isinstance(value, Mapping):
        text = "{" + ", ".join(f"{k!r}: {redact(str(k), v, limit)}" for k, v in value.items()) + "}"
    else:
        text = repr(value)
    return text if len(text) <= limit else text[:limit - 1] + "…"


def _frames(exc: BaseException) -> list[dict[str, Any]]:
    frames = []
    tb: TracebackType | None = exc.__traceback__
    while tb is not None:
        frame = tb.tb_frame
        frames.append({"file": Path(frame.f_code.co_filename).name, "line": tb.tb_lineno,
                       "function": frame.f_code.co_name,
                       "locals": {k: redact(k, v) for k, v in frame.f_locals.items() if not k.startswith("__")}})
        tb = tb.tb_next
    return frames


def crash_report(exc: BaseException, *, app_version: str = "4.2.0") -> dict[str, Any]:
    """JSON-ready dict: type, message, notes, frames with redacted locals, causes and sub-exceptions."""
    report: dict[str, Any] = {
        "type": type(exc).__qualname__,
        "message": str(exc),
        "notes": list(getattr(exc, "__notes__", [])),
        "frames": _frames(exc),
        "app_version": app_version,
        "python": sys.version.split()[0],
    }
    if exc.__cause__ is not None:
        report["cause"] = crash_report(exc.__cause__, app_version=app_version)
    elif exc.__context__ is not None and not exc.__suppress_context__:
        report["context"] = crash_report(exc.__context__, app_version=app_version)
    if isinstance(exc, BaseExceptionGroup):
        report["exceptions"] = [crash_report(e, app_version=app_version) for e in exc.exceptions]
    report["text"] = "".join(traceback.TracebackException.from_exception(exc).format())
    return report


def add_context(**context: Any) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Decorator: annotate any escaping exception with *what we were doing* (PEP 678 notes)."""

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            try:
                return func(*args, **kwargs)
            except Exception as exc:
                details = ", ".join(f"{k}={redact(k, v)}" for k, v in {**context, **kwargs}.items())
                exc.add_note(f"while running {func.__name__}({details})")
                raise

        return wrapper

    return decorator


def install_crash_hooks(report_dir: Path, *, on_crash: Callable[[Path], None] | None = None) -> Callable[[], None]:
    """Write a JSON crash file for uncaught errors in *any* thread; returns an uninstall function."""
    report_dir.mkdir(parents=True, exist_ok=True)
    counter = itertools.count(1)
    old_sys, old_thread = sys.excepthook, threading.excepthook

    def write(exc: BaseException, thread: str) -> None:
        path = report_dir / f"crash-{next(counter):03d}.json"
        path.write_text(json.dumps({**crash_report(exc), "thread": thread}, indent=2, default=str), encoding="utf-8")
        if on_crash:
            on_crash(path)

    def sys_hook(exc_type: type[BaseException], exc: BaseException, tb: TracebackType | None) -> None:
        if issubclass(exc_type, KeyboardInterrupt):
            return old_sys(exc_type, exc, tb)  # Ctrl+C is not a crash
        write(exc, "MainThread")

    def thread_hook(args: threading.ExceptHookArgs) -> None:
        if args.exc_value is not None:
            write(args.exc_value, args.thread.name if args.thread else "?")

    sys.excepthook, threading.excepthook = sys_hook, thread_hook

    def uninstall() -> None:
        sys.excepthook, threading.excepthook = old_sys, old_thread

    return uninstall


@dataclass
class CallTracer:
    """A tiny profiler-style debugger: records calls/returns in chosen modules via ``sys.settrace``."""

    module_filter: str = ""
    events: list[str] = field(default_factory=list)
    depth: int = 0

    def _trace(self, frame: FrameType, event: str, arg: Any) -> Callable[..., Any] | None:
        if self.module_filter not in frame.f_globals.get("__name__", ""):
            return None  # don't trace into other modules at all
        name = frame.f_code.co_name
        if event == "call":
            args = ", ".join(f"{k}={redact(k, frame.f_locals[k])}"
                             for k in frame.f_code.co_varnames[:frame.f_code.co_argcount])
            self.events.append(f"{'  ' * self.depth}→ {name}({args})")
            self.depth += 1
            return self._trace
        if event == "return":
            self.depth -= 1
            self.events.append(f"{'  ' * self.depth}← {name} = {redact('result', arg)}")
        elif event == "exception":
            self.events.append(f"{'  ' * self.depth}! {name} raised {arg[0].__name__}")
        return self._trace

    @contextmanager
    def tracing(self) -> Iterator[CallTracer]:
        previous = sys.gettrace()
        sys.settrace(self._trace)
        try:
            yield self
        finally:
            sys.settrace(previous)


class Watchpoint(bdb.Bdb):
    """Steps through ``func`` line by line and records each change of ``variable`` (a 'data breakpoint')."""

    def __init__(self, variable: str, func_name: str) -> None:
        super().__init__()
        self.variable, self.func_name = variable, func_name
        self.changes: list[tuple[int, Any]] = []
        self._last: Any = object()

    def user_line(self, frame: FrameType) -> None:
        if frame.f_code.co_name == self.func_name and self.variable in frame.f_locals:
            value = frame.f_locals[self.variable]
            if value != self._last:
                self.changes.append((frame.f_lineno, value))
                self._last = value

    def user_return(self, frame: FrameType, return_value: Any) -> None:
        self.user_line(frame)  # catch a change on the function's last line

    def watch(self, func: Callable[..., R], *args: Any) -> R:
        return cast(R, self.runcall(func, *args))


# --- spans: a pocket-sized tracing API --------------------------------------------
_current_span: contextvars.ContextVar[tuple[str, str] | None] = contextvars.ContextVar("span", default=None)
_ids = itertools.count(1)


@contextmanager
def span(name: str, sink: Callable[[str], None], **attrs: Any) -> Iterator[dict[str, Any]]:
    """Nested spans share a trace id; each emits one JSON log line with its duration and outcome."""
    parent = _current_span.get()
    trace_id = parent[0] if parent else f"t{next(_ids):04d}"
    span_id = f"s{next(_ids):04d}"
    token = _current_span.set((trace_id, span_id))
    record: dict[str, Any] = {"trace": trace_id, "span": span_id, "parent": parent[1] if parent else None,
                              "name": name, **{k: redact(k, v) for k, v in attrs.items()}}
    start = time.perf_counter()
    try:
        yield record
        record["status"] = "ok"
    except Exception as exc:
        record["status"] = "error"
        record["error"] = f"{type(exc).__name__}: {exc}"
        raise
    finally:
        record["ms"] = round((time.perf_counter() - start) * 1000, 2)
        _current_span.reset(token)
        sink(json.dumps(record))


# --- the 'photo editor' code we debug ---------------------------------------------
def apply_filter(pixels: list[int], gain: float) -> list[int]:
    return [min(255, int(p * gain)) for p in pixels]


def brightness(pixels: list[int]) -> float:
    return sum(pixels) / len(pixels)


@add_context(feature="export")
def export_image(pixels: list[int], fmt: str, api_token: str = "tok-123") -> bytes:
    if fmt not in {"png", "jpg"}:
        raise ValueError(f"unsupported format {fmt!r}")
    adjusted = apply_filter(pixels, 1.2)
    return bytes(adjusted) if brightness(adjusted) else b""


def running_total(values: list[int]) -> int:
    total = 0
    for v in values:
        total += v
    return total


def main() -> None:
    print("Day 99 – Observability & debugging toolkit\n")
    try:
        export_image([10, 20], "tiff", api_token="tok-secret")
    except ValueError as exc:
        report = crash_report(exc)
        print("crash:", report["type"], report["message"], report["notes"])
        print("frame locals:", report["frames"][-1]["locals"])
    tracer = CallTracer(module_filter=__name__)
    with tracer.tracing():
        export_image([100, 200], "png")
    print("\n".join(tracer.events))
    watch = Watchpoint("total", "running_total")
    print("watch total:", watch.watch(running_total, [3, 4, 5]), watch.changes)
    lines: list[str] = []
    with span("export", lines.append, fmt="png"), span("encode", lines.append, api_key="k"):
        apply_filter([1, 2, 3], 2)
    print("\n".join(lines))


if __name__ == "__main__":
    main()
