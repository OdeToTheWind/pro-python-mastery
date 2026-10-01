"""Day 65 – Generators & ``yield``.

Scenario: a *smart-meter energy monitor* that streams millions of readings.
Generators process them one at a time, so memory stays flat no matter how
large the stream is.

Deliverables (syllabus):
* Generator functions (``yield``)
* Lazy evaluation (work happens only when a value is requested)
* Memory benefits (measured, not just claimed)
"""

from __future__ import annotations

import itertools
import sys
import tracemalloc
from collections.abc import Callable, Iterable, Iterator

DELIVERABLES: dict[str, str] = {
    "generator function with yield": "meter_readings",
    "infinite generator + islice": "meter_readings",
    "lazy evaluation (proved with a log)": "traced_readings",
    "generator expression": "kwh_total",
    "generator state is paused between yields": "peak_detector",
    "memory benefits (getsizeof)": "container_sizes",
    "memory benefits (tracemalloc)": "peak_memory_kib",
    "generators are single-use": "single_use_demo",
}


def meter_readings(start_watts: int = 500, step: int = 37, modulus: int = 2000) -> Iterator[int]:
    """An endless, deterministic stream of power readings in watts."""
    value = start_watts
    while True:  # infinite is fine: the caller decides how many to take
        yield value
        value = (value * 7 + step) % modulus


def traced_readings(values: Iterable[int], log: list[str]) -> Iterator[int]:
    """Logs when each value is *produced* – proves nothing runs ahead of time."""
    log.append("generator created – no work yet")
    for value in values:
        log.append(f"produced {value}")
        yield value
    log.append("exhausted")


def kwh_total(watts: Iterable[int], seconds_per_reading: int = 60) -> float:
    """A generator expression feeds ``sum`` one value at a time."""
    return round(sum(w * seconds_per_reading / 3_600_000 for w in watts), 4)


def peak_detector(watts: Iterable[int], threshold: int) -> Iterator[tuple[int, int]]:
    """Yield (index, value) for spikes; local variables survive between yields."""
    previous = None
    for index, value in enumerate(watts):
        if previous is not None and value - previous >= threshold:
            yield index, value
        previous = value


def container_sizes(n: int) -> dict[str, int]:
    """A list stores n results; a generator stores only its paused frame."""
    return {
        "list": sys.getsizeof([i * i for i in range(n)]),
        "generator": sys.getsizeof(i * i for i in range(n)),
    }


def peak_memory_kib(build: Callable[[], object]) -> float:
    """Peak memory allocated while running *build* (tracemalloc)."""
    tracemalloc.start()
    try:
        build()
        _, peak = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()
    return round(peak / 1024, 1)


def single_use_demo() -> tuple[int, int]:
    squares = (n * n for n in range(5))
    first_pass = sum(squares)
    second_pass = sum(squares)  # already exhausted → 0
    return first_pass, second_pass


def main() -> None:
    print("Day 65 – Smart-meter stream\n")
    first_five = list(itertools.islice(meter_readings(), 5))
    print("first 5 readings:", first_five)
    log: list[str] = []
    stream = traced_readings(first_five, log)
    print("after creating the generator:", log)
    next(stream)
    print("after one next():", log)
    print("energy for 1 000 readings:", kwh_total(itertools.islice(meter_readings(), 1000)), "kWh")
    print("spikes ≥ 800 W:", list(itertools.islice(peak_detector(meter_readings(), 800), 3)))
    print("sizes for 1 000 000 items:", container_sizes(1_000_000))
    n = 200_000
    print(f"peak KiB  list={peak_memory_kib(lambda: sum([i for i in range(n)]))}  "
          f"generator={peak_memory_kib(lambda: sum(i for i in range(n)))}")
    print("single use:", single_use_demo())


if __name__ == "__main__":
    main()
