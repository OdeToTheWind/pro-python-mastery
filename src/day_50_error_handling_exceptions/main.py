"""Day 50 – Error Handling and Exceptions (advanced techniques).

Scenario: a *configuration loader for a microservice* that reads JSON from
disk, validates many fields at once, retries flaky reads and logs failures
with full context.

Deliverables (syllabus):
* Advanced exception handling techniques: chaining (``raise ... from``),
  ``ExceptionGroup`` / ``except*``, ``add_note()``, ``contextlib.suppress``,
  re-raising, retries
* Best practices: catch narrowly, keep context, log with ``logging.exception``,
  clean up with ``finally`` / context managers
"""

from __future__ import annotations

import contextlib
import json
import logging
import time
from collections.abc import Callable
from pathlib import Path
from typing import Any

DELIVERABLES: dict[str, str] = {
    "exception chaining (raise from)": "parse_config",
    "add_note() for extra context": "parse_config",
    "ExceptionGroup for multiple errors": "validate_config",
    "except* to handle groups by type": "load_service_config",
    "retry with backoff": "retry",
    "contextlib.suppress": "remove_stale_lock",
    "logging.exception best practice": "load_service_config",
}

log = logging.getLogger("config")
REQUIRED = {"service": str, "port": int, "workers": int}


class ConfigError(Exception):
    """Raised for any problem with the service configuration."""


def parse_config(text: str, source: str = "<string>") -> dict[str, Any]:
    """Wrap the low-level error but keep it as ``__cause__`` for debugging."""
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        error = ConfigError(f"{source} is not valid JSON")
        error.add_note(f"line {exc.lineno}, column {exc.colno}: {exc.msg}")
        raise error from exc
    if not isinstance(data, dict):
        raise ConfigError(f"{source} must contain a JSON object")
    return data


def validate_config(config: dict[str, Any]) -> dict[str, Any]:
    """Report *every* problem at once with an ``ExceptionGroup``."""
    problems: list[Exception] = []
    for key, expected in REQUIRED.items():
        if key not in config:
            problems.append(KeyError(f"missing {key!r}"))
        elif not isinstance(config[key], expected) or isinstance(config[key], bool):
            problems.append(TypeError(f"{key!r} must be {expected.__name__}"))
    port = config.get("port")
    if isinstance(port, int) and not 1 <= port <= 65535:
        problems.append(ValueError("'port' must be 1–65535"))
    if problems:
        raise ExceptionGroup("invalid configuration", problems)
    return config


def retry[T](func: Callable[[], T], *, attempts: int = 3, delay: float = 0.1,
             retry_on: tuple[type[Exception], ...] = (OSError,),
             sleep: Callable[[float], None] = time.sleep) -> T:
    """Retry only *transient* errors, with exponential backoff; re-raise the last one."""
    for attempt in range(1, attempts + 1):
        try:
            return func()
        except retry_on as exc:
            if attempt == attempts:
                raise
            log.warning("attempt %d failed (%s); retrying", attempt, exc)
            sleep(delay * 2 ** (attempt - 1))
    raise AssertionError("unreachable")  # pragma: no cover


def remove_stale_lock(lock: Path) -> None:
    """``suppress`` states intent: a missing lock file is fine."""
    with contextlib.suppress(FileNotFoundError):
        lock.unlink()


def load_service_config(path: Path, read: Callable[[Path], str] | None = None) -> tuple[dict[str, Any] | None, list[str]]:
    """Load + validate. Returns (config or None, human-readable problems)."""
    reader = read or (lambda p: p.read_text(encoding="utf-8"))
    messages: list[str] = []
    try:
        text = retry(lambda: reader(path), retry_on=(TimeoutError,), sleep=lambda _s: None)
        return validate_config(parse_config(text, path.name)), messages
    except* (KeyError, TypeError) as group:
        messages += [f"schema: {e.args[0]}" for e in group.exceptions]
    except* ValueError as group:
        messages += [f"value: {e}" for e in group.exceptions]
    except* ConfigError as group:
        for exc in group.exceptions:
            log.exception("could not parse %s", path)  # logs the traceback *and* the cause
            messages.append(f"parse: {exc} ({'; '.join(getattr(exc, '__notes__', []))})")
    except* FileNotFoundError:
        messages.append(f"missing: {path.name}")
    return None, messages


def main() -> None:
    import tempfile

    logging.basicConfig(level=logging.CRITICAL)
    print("Day 50 – Service configuration loader\n")
    with tempfile.TemporaryDirectory() as tmp:
        folder = Path(tmp)
        cases = {
            "good.json": '{"service": "api", "port": 8080, "workers": 4}',
            "broken.json": '{"service": "api", "port": 80,,}',
            "invalid.json": '{"service": 7, "port": 99999}',
        }
        for name, text in cases.items():
            (folder / name).write_text(text, encoding="utf-8")
        for name in [*cases, "absent.json"]:
            config, problems = load_service_config(folder / name)
            print(f"{name:<13} → {config or problems}")
        remove_stale_lock(folder / "service.lock")
        print("stale lock removal is a no-op when absent ✔")


if __name__ == "__main__":
    main()
