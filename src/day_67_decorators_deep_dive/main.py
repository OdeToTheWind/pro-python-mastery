"""Day 67 – Decorators Deep Dive.

Scenario: a *weather-service client toolkit* – cross-cutting concerns
(timing, retries, caching per city, rate limiting, input validation) are
added to plain functions with decorators instead of being copy-pasted.

Deliverables (syllabus):
* Function decorators (wrappers that add behaviour)
* ``functools.wraps`` (preserving name, docstring, signature)
* Parameterised decorators (decorator factories)
* Class-based decorators (state kept on an instance)
"""

from __future__ import annotations

import functools
import inspect
import time
from collections.abc import Callable
from typing import Any

DELIVERABLES: dict[str, str] = {
    "function decorator": "timed",
    "@wraps preserves metadata": "timed",
    "decorator without wraps (the problem)": "naive_timed",
    "parameterised decorator": "retry",
    "decorator usable with and without arguments": "validate_range",
    "class-based decorator with state": "RateLimit",
    "decorator for caching": "memoize_by",
    "stacking order": "STACKING_ORDER",
}

Func = Callable[..., Any]
STACKING_ORDER: list[str] = []


def naive_timed(func: Func) -> Func:
    """Works, but hides the original function's identity (no ``@wraps``)."""

    def wrapper(*args: Any, **kwargs: Any) -> Any:
        return func(*args, **kwargs)

    return wrapper


def timed(func: Func) -> Func:
    """Record the duration of every call in ``wrapper.timings`` (seconds)."""

    @functools.wraps(func)  # copies __name__, __doc__, __qualname__, __wrapped__ …
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            wrapper.timings.append(time.perf_counter() - start)  # type: ignore[attr-defined]

    wrapper.timings = []  # type: ignore[attr-defined]
    return wrapper


def retry(times: int = 3, *, exceptions: tuple[type[Exception], ...] = (ConnectionError,),
          delay: float = 0.0, sleep: Callable[[float], None] = time.sleep) -> Callable[[Func], Func]:
    """Decorator *factory*: ``@retry(times=5)`` returns the actual decorator."""
    if times < 1:
        raise ValueError("times must be at least 1")

    def decorator(func: Func) -> Func:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    if attempt == times:
                        raise
                    sleep(delay * attempt)
            raise AssertionError("unreachable")  # pragma: no cover

        return wrapper

    return decorator


def validate_range(func: Func | None = None, *, low: float = -90.0, high: float = 90.0) -> Any:
    """Check the first argument is within bounds; usable as ``@validate_range`` *or*
    ``@validate_range(low=0, high=100)``."""

    def decorator(inner: Func) -> Func:
        @functools.wraps(inner)
        def wrapper(value: float, *args: Any, **kwargs: Any) -> Any:
            if not low <= value <= high:
                raise ValueError(f"{inner.__name__}: {value} not in [{low}, {high}]")
            return inner(value, *args, **kwargs)

        return wrapper

    return decorator(func) if func is not None else decorator


class RateLimit:
    """Class-based decorator: the *instance* keeps call history between calls."""

    def __init__(self, calls: int, per_seconds: float, clock: Callable[[], float] = time.monotonic) -> None:
        self.calls, self.per_seconds, self.clock = calls, per_seconds, clock
        self.history: list[float] = []

    def __call__(self, func: Func) -> Func:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            now = self.clock()
            self.history = [t for t in self.history if now - t < self.per_seconds]
            if len(self.history) >= self.calls:
                raise RuntimeError(f"rate limit: {self.calls} calls per {self.per_seconds}s")
            self.history.append(now)
            return func(*args, **kwargs)

        wrapper.limiter = self  # type: ignore[attr-defined]
        return wrapper


def memoize_by(key: Callable[..., Any]) -> Callable[[Func], Func]:
    """Cache results under a custom key (e.g. case-insensitive city names)."""

    def decorator(func: Func) -> Func:
        cache: dict[Any, Any] = {}

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            k = key(*args, **kwargs)
            if k not in cache:
                cache[k] = func(*args, **kwargs)
            return cache[k]

        wrapper.cache = cache  # type: ignore[attr-defined]
        return wrapper

    return decorator


def tag(label: str) -> Callable[[Func], Func]:
    """Records the order in which stacked decorators *run* at call time."""

    def decorator(func: Func) -> Func:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            STACKING_ORDER.append(label)
            return func(*args, **kwargs)

        return wrapper

    return decorator


@tag("outer")
@tag("inner")
def stacked() -> str:
    """Decorators apply bottom-up but their wrappers run top-down."""
    return "done"


@timed
@memoize_by(lambda city: city.strip().casefold())
def forecast(city: str) -> str:
    """Pretend to call a slow weather API for *city*."""
    return f"{city.strip().title()}: 21°C, light breeze"


@validate_range
def describe_latitude(lat: float) -> str:
    return "northern" if lat > 0 else "southern" if lat < 0 else "equator"


def main() -> None:
    print("Day 67 – Weather-client decorators\n")
    print(forecast("berlin"), "|", forecast("  BERLIN "), "| cache:", forecast.cache)  # type: ignore[attr-defined]
    print("wraps kept the docstring:", forecast.__doc__)
    print("signature:", inspect.signature(forecast), "| naive name:", naive_timed(forecast).__name__)
    print("latitude 52.5 →", describe_latitude(52.5))
    STACKING_ORDER.clear()
    stacked()
    print("stacking run order:", STACKING_ORDER)

    attempts: list[int] = []

    @retry(times=3, delay=0)
    def flaky() -> str:
        attempts.append(1)
        if len(attempts) < 3:
            raise ConnectionError("timeout")
        return "ok"

    print("retry:", flaky(), "after", len(attempts), "attempts")


if __name__ == "__main__":
    main()
