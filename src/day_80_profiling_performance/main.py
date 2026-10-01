"""Day 80 – Profiling & Performance.

Scenario: an *e-commerce nightly report* that got slow as the shop grew. We
measure first (``cProfile``, ``timeit``, ``tracemalloc``/``memory_profiler``),
find the hotspots, then apply targeted optimisation patterns – and prove the
fast version returns exactly the same answer.

Deliverables (syllabus):
* ``cProfile`` + ``pstats`` (find where time goes)
* ``timeit`` (compare small alternatives fairly)
* ``memory_profiler`` (process memory over time) and ``tracemalloc`` (Python allocations)
* Optimisation patterns: right data structure, avoid repeated work, builtins,
  ``str.join``, generators, caching
"""

from __future__ import annotations

import cProfile
import io
import pstats
import timeit
import tracemalloc
from collections import Counter
from collections.abc import Callable, Iterable, Iterator
from dataclasses import dataclass
from functools import cache

DELIVERABLES: dict[str, str] = {
    "cProfile + pstats hotspots": "profile_hotspots",
    "timeit comparisons": "compare_timings",
    "memory_profiler": "memory_profile",
    "tracemalloc": "peak_allocation_kib",
    "pattern: set membership instead of list": "report_fast",
    "pattern: str.join instead of +=": "render_csv_fast",
    "pattern: cache repeated work": "tax_rate",
    "pattern: generators for streaming": "order_totals",
}


@dataclass(frozen=True, slots=True)
class Order:
    order_id: int
    customer: str
    country: str
    amount_cents: int


def make_orders(n: int) -> list[Order]:
    countries = ["DE", "FR", "IN", "US", "NL"]
    return [Order(i, f"cust{(i * 7919) % (n // 3 + 1)}", countries[i % 5], 500 + (i * 37) % 9000) for i in range(n)]


def slow_tax_rate(country: str) -> float:
    """Pretend lookup that is expensive (e.g. parsing a rules file each time)."""
    rules = {c: r for c, r in (("DE", 0.19), ("FR", 0.20), ("IN", 0.18), ("US", 0.0), ("NL", 0.21))}
    total = 0
    for _ in range(200):  # simulated cost
        total += len(rules)
    return rules[country]


@cache
def tax_rate(country: str) -> float:
    return slow_tax_rate(country)


# --------------------------------------------------------------------------- slow version

def report_slow(orders: list[Order]) -> dict[str, object]:
    seen_customers: list[str] = []
    repeat_buyers = 0
    gross = 0.0
    for order in orders:
        if order.customer in seen_customers:  # O(n) scan of a list → O(n²) overall
            repeat_buyers += 1
        else:
            seen_customers.append(order.customer)
        gross += order.amount_cents * (1 + slow_tax_rate(order.country))  # recomputed every time
    return {"customers": len(seen_customers), "repeat_orders": repeat_buyers, "gross_cents": round(gross)}


def render_csv_slow(orders: Iterable[Order]) -> str:
    text = "id,customer,amount\n"
    for order in orders:
        text += f"{order.order_id},{order.customer},{order.amount_cents}\n"  # copies the string each time
    return text


# --------------------------------------------------------------------------- fast version

def order_totals(orders: Iterable[Order]) -> Iterator[float]:
    """Generator: totals are produced one at a time, never stored in a list."""
    for order in orders:
        yield order.amount_cents * (1 + tax_rate(order.country))


def report_fast(orders: list[Order]) -> dict[str, object]:
    counts = Counter(order.customer for order in orders)  # one pass, hashing → O(n)
    return {"customers": len(counts), "repeat_orders": len(orders) - len(counts),
            "gross_cents": round(sum(order_totals(orders)))}


def render_csv_fast(orders: Iterable[Order]) -> str:
    return "id,customer,amount\n" + "".join(f"{o.order_id},{o.customer},{o.amount_cents}\n" for o in orders)


# --------------------------------------------------------------------------- measuring

def profile_hotspots(func: Callable[[], object], top: int = 5) -> list[tuple[str, int, float]]:
    """Return (function name, call count, cumulative seconds) for the top entries."""
    profiler = cProfile.Profile()
    profiler.enable()
    func()
    profiler.disable()
    stats = pstats.Stats(profiler, stream=io.StringIO()).sort_stats(pstats.SortKey.CUMULATIVE)
    rows = []
    for (filename, _line, name), (_cc, ncalls, _tt, cumtime, _callers) in stats.stats.items():  # type: ignore[attr-defined]
        if filename == __file__:
            rows.append((name, ncalls, cumtime))
    return sorted(rows, key=lambda r: r[2], reverse=True)[:top]


def compare_timings(candidates: dict[str, Callable[[], object]], number: int = 3, repeat: int = 3) -> dict[str, float]:
    """``timeit.repeat`` and take the *minimum*: the least noisy estimate of the cost."""
    return {name: min(timeit.repeat(func, number=number, repeat=repeat)) / number for name, func in candidates.items()}


def peak_allocation_kib(func: Callable[[], object]) -> float:
    tracemalloc.start()
    try:
        func()
        return tracemalloc.get_traced_memory()[1] / 1024
    finally:
        tracemalloc.stop()


def memory_profile(func: Callable[[], object], interval: float = 0.01) -> dict[str, float]:
    """``memory_profiler.memory_usage`` samples the process's memory while *func* runs."""
    from memory_profiler import memory_usage

    samples = memory_usage((func, (), {}), interval=interval, max_iterations=1)
    return {"samples": float(len(samples)), "peak_mib": round(max(samples), 1),
            "growth_mib": round(max(samples) - samples[0], 1)}


def main() -> None:
    orders = make_orders(6000)
    print("Day 80 – Speeding up the nightly report\n")
    assert report_slow(orders) == report_fast(orders)
    print("same answer:", report_fast(orders))
    print("\ncProfile of the slow report (cumulative s):")
    for name, calls, cumtime in profile_hotspots(lambda: report_slow(orders)):
        print(f"  {name:<18} {calls:>7} calls {cumtime:8.4f}s")
    timings = compare_timings({"slow": lambda: report_slow(orders), "fast": lambda: report_fast(orders)}, number=1)
    print(f"\ntimeit: slow {timings['slow']:.4f}s, fast {timings['fast']:.4f}s → {timings['slow'] / timings['fast']:.0f}× faster")
    print("tracemalloc peak KiB – list of totals vs generator:",
          round(peak_allocation_kib(lambda: sum([o.amount_cents * 1.2 for o in orders])), 1),
          round(peak_allocation_kib(lambda: sum(order_totals(orders))), 1))
    print("memory_profiler:", memory_profile(lambda: [bytes(1024) for _ in range(20_000)]))


if __name__ == "__main__":
    main()
