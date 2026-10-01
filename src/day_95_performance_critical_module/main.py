"""Day 95 – Capstone: Performance-critical Module.

Scenario: a *ride-hailing dispatcher* must find the nearest free driver for
every waiting rider, city-wide, several times per second. The same
haversine matching is implemented four ways – naive Python, tuned Python
with a spatial grid index, vectorised NumPy and (optionally) Numba – then
profiled, benchmarked and cross-checked so every fast path returns exactly
what the slow, obviously-correct version returns.

Deliverables (syllabus):
* Profiling the baseline (``cProfile`` + ``pstats`` → the hotspot)
* Optimisation in pure Python (precomputation, local names, grid index)
* Vectorisation with NumPy (broadcasting, ``argmin``)
* Optional Numba JIT with a graceful fallback, plus a benchmark harness
"""

from __future__ import annotations

import cProfile
import io
import math
import pstats
import random
import timeit
from collections import defaultdict
from collections.abc import Callable, Iterable, Sequence
from functools import partial

import numpy as np

try:  # optional accelerator: the module works (just slower) without it
    from numba import njit  # type: ignore[import-not-found]

    HAS_NUMBA = True
except ImportError:  # pragma: no cover - depends on the environment
    HAS_NUMBA = False

DELIVERABLES: dict[str, str] = {
    "baseline (obviously correct)": "nearest_naive",
    "profiling the baseline": "profile_hotspots",
    "pure-Python optimisation with a grid index": "nearest_grid",
    "NumPy vectorisation": "nearest_numpy",
    "optional Numba JIT with fallback": "nearest_numba",
    "benchmark harness": "benchmark",
}

EARTH_KM = 6371.0
Point = tuple[float, float]  # (lat, lon) in degrees


def haversine(a: Point, b: Point) -> float:
    lat1, lon1, lat2, lon2 = map(math.radians, (*a, *b))
    h = math.sin((lat2 - lat1) / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin((lon2 - lon1) / 2) ** 2
    return 2 * EARTH_KM * math.asin(math.sqrt(h))


def nearest_naive(riders: Sequence[Point], drivers: Sequence[Point]) -> list[int]:
    """O(riders × drivers) and recomputes every radian conversion – the reference answer."""
    result = []
    for rider in riders:
        distances = [haversine(rider, driver) for driver in drivers]
        result.append(distances.index(min(distances)))
    return result


def nearest_grid(riders: Sequence[Point], drivers: Sequence[Point], cell_deg: float = 0.02) -> list[int]:
    """Bucket drivers into grid cells, search outward ring by ring, stop once no closer cell can exist."""
    if not drivers:
        raise ValueError("no drivers")
    rad = math.radians
    cos, sin, asin, sqrt = math.cos, math.sin, math.asin, math.sqrt  # local names: faster lookups
    pre = [(rad(lat), rad(lon), cos(rad(lat))) for lat, lon in drivers]
    grid: dict[tuple[int, int], list[int]] = defaultdict(list)
    for j, (lat, lon) in enumerate(drivers):
        grid[(int(lat // cell_deg), int(lon // cell_deg))].append(j)
    cell_km = cell_deg * math.pi / 180 * EARTH_KM  # the smallest a cell can be (north–south)

    def nearest_one(lat: float, lon: float) -> int:
        rlat, rlon, rcos = rad(lat), rad(lon), cos(rad(lat))
        ci, cj = int(lat // cell_deg), int(lon // cell_deg)
        best, best_j = math.inf, -1

        def scan(candidates: Iterable[int]) -> None:
            nonlocal best, best_j
            for j in candidates:
                dlat, dlon, dcos = pre[j]
                h = sin((dlat - rlat) / 2) ** 2 + rcos * dcos * sin((dlon - rlon) / 2) ** 2
                d = 2 * EARTH_KM * asin(sqrt(h))
                if d < best or (d == best and j < best_j):
                    best, best_j = d, j

        ring = 0
        while True:
            if (2 * ring + 1) ** 2 > 4 * len(grid):  # sparse area: rings cost more than a full scan
                scan(range(len(drivers)))
                return best_j
            for di in range(-ring, ring + 1):
                for dj in (range(-ring, ring + 1) if abs(di) == ring else (-ring, ring)):
                    scan(grid.get((ci + di, cj + dj), ()))
            # anything in ring+1 is at least `ring` whole cells away (scaled by longitude shrinkage)
            if best_j >= 0 and ring * cell_km * min(1.0, rcos) > best:
                return best_j
            ring += 1

    return [nearest_one(lat, lon) for lat, lon in riders]


def _distance_matrix(riders: np.ndarray, drivers: np.ndarray) -> np.ndarray:
    r = np.radians(riders)[:, None, :]  # shape (R, 1, 2)
    d = np.radians(drivers)[None, :, :]  # shape (1, D, 2) → broadcasting gives (R, D)
    dlat, dlon = d[..., 0] - r[..., 0], d[..., 1] - r[..., 1]
    h = np.sin(dlat / 2) ** 2 + np.cos(r[..., 0]) * np.cos(d[..., 0]) * np.sin(dlon / 2) ** 2
    return 2 * EARTH_KM * np.arcsin(np.sqrt(h))


def nearest_numpy(riders: Sequence[Point], drivers: Sequence[Point], batch: int = 512) -> list[int]:
    """Batches of riders keep the (R × D) matrix bounded in memory."""
    if not drivers:
        raise ValueError("no drivers")
    d = np.asarray(drivers, dtype=np.float64)
    r_all = np.asarray(riders, dtype=np.float64).reshape(-1, 2)
    out: list[int] = []
    for start in range(0, len(r_all), batch):
        out += np.argmin(_distance_matrix(r_all[start:start + batch], d), axis=1).tolist()
    return out


def _numba_kernel(r: np.ndarray, d: np.ndarray) -> np.ndarray:  # pragma: no cover - compiled when numba exists
    out = np.empty(r.shape[0], dtype=np.int64)
    for i in range(r.shape[0]):
        best, best_j = np.inf, -1
        for j in range(d.shape[0]):
            h = (np.sin((d[j, 0] - r[i, 0]) / 2) ** 2
                 + np.cos(r[i, 0]) * np.cos(d[j, 0]) * np.sin((d[j, 1] - r[i, 1]) / 2) ** 2)
            dist = 2 * EARTH_KM * np.arcsin(np.sqrt(h))
            if dist < best:
                best, best_j = dist, j
        out[i] = best_j
    return out


_compiled = njit(cache=False)(_numba_kernel) if HAS_NUMBA else None


def nearest_numba(riders: Sequence[Point], drivers: Sequence[Point]) -> list[int]:
    """Uses the JIT kernel when Numba is installed, otherwise falls back to NumPy."""
    if _compiled is None:
        return nearest_numpy(riders, drivers)
    if not drivers:  # pragma: no cover
        raise ValueError("no drivers")
    r = np.radians(np.asarray(riders, dtype=np.float64).reshape(-1, 2))  # pragma: no cover
    return list(map(int, _compiled(r, np.radians(np.asarray(drivers, dtype=np.float64)))))  # pragma: no cover


def random_city(n: int, seed: int, centre: Point = (38.72, -9.14), spread: float = 0.08) -> list[Point]:
    rng = random.Random(seed)
    return [(centre[0] + rng.uniform(-spread, spread), centre[1] + rng.uniform(-spread, spread)) for _ in range(n)]


def profile_hotspots(func: Callable[[], object], top: int = 5) -> list[tuple[str, int]]:
    """Return (function name, call count) for the most expensive functions by own time."""
    profiler = cProfile.Profile()
    profiler.runcall(func)
    stats = pstats.Stats(profiler, stream=io.StringIO()).sort_stats(pstats.SortKey.TIME)
    rows = sorted(stats.stats.items(), key=lambda item: item[1][2], reverse=True)  # type: ignore[attr-defined]
    return [(f"{key[2]}", value[1]) for key, value in rows[:top]]


def benchmark(riders: Sequence[Point], drivers: Sequence[Point], repeat: int = 3) -> dict[str, float]:
    """Best-of-N milliseconds; every implementation must agree with the baseline first."""
    impls = {"naive": nearest_naive, "grid": nearest_grid, "numpy": nearest_numpy, "numba": nearest_numba}
    expected = nearest_naive(riders, drivers)
    timings = {}
    for name, impl in impls.items():
        if impl(riders, drivers) != expected:
            raise AssertionError(f"{name} disagrees with the baseline")
        best = min(timeit.repeat(partial(impl, riders, drivers), number=1, repeat=repeat))
        timings[name] = round(best * 1000, 2)
    return timings


def main() -> None:
    print("Day 95 – Nearest-driver matching\n")
    riders, drivers = random_city(200, 1), random_city(800, 2)
    print("hotspots (naive):", profile_hotspots(lambda: nearest_naive(riders[:20], drivers), top=3))
    timings = benchmark(riders, drivers, repeat=2)
    for name, ms in timings.items():
        print(f"  {name:<6} {ms:9.2f} ms  ({timings['naive'] / ms:5.1f}× faster than naive)")
    print("numba available:", HAS_NUMBA)


if __name__ == "__main__":
    main()
