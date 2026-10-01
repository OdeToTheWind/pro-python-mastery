"""Day 74 – Concurrency: Multiprocessing.

Scenario: a *satellite-image analysis lab*. Counting "bright pixels" in large
tiles is pure CPU work, so it runs in a process pool (each process has its own
interpreter and GIL). Tiles are shared through ``shared_memory`` instead of
being copied, and a small advisor decides when processes beat threads.

Deliverables (syllabus):
* Process pools (``ProcessPoolExecutor``, ``multiprocessing.Pool``)
* Shared memory (``multiprocessing.shared_memory``, ``Value`` with a lock)
* Choosing processes vs threads (and measuring the overhead)
"""

from __future__ import annotations

import multiprocessing as mp
import os
import time
from collections.abc import Callable
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass
from multiprocessing import shared_memory

DELIVERABLES: dict[str, str] = {
    "ProcessPoolExecutor": "analyse_tiles",
    "multiprocessing.Pool with chunksize": "analyse_tiles_pool",
    "shared_memory (zero-copy buffers)": "bright_pixels_shared",
    "shared Value with a lock": "count_with_shared_value",
    "processes vs threads decision": "choose_executor",
    "measuring speed-up and overhead": "benchmark",
}


def make_tile(seed: int, size: int = 200_000) -> bytes:
    """Deterministic pseudo-random 'pixel' bytes (no numpy needed)."""
    value, out = seed or 1, bytearray(size)
    for i in range(size):
        value = (value * 1103515245 + 12345) & 0x7FFFFFFF
        out[i] = value >> 23
    return bytes(out)


def bright_pixels(tile: bytes, threshold: int = 200) -> int:
    """CPU-bound: a pure-Python loop over every byte."""
    return sum(1 for pixel in tile if pixel >= threshold)


def analyse_tiles(tiles: list[bytes], workers: int | None = None) -> list[int]:
    """Submit each tile to a process; results are collected as they finish, then re-ordered."""
    results: dict[int, int] = {}
    with ProcessPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(bright_pixels, tile): index for index, tile in enumerate(tiles)}
        for future in as_completed(futures):
            results[futures[future]] = future.result()
    return [results[i] for i in range(len(tiles))]


def analyse_tiles_pool(tiles: list[bytes], workers: int = 2) -> list[int]:
    """The classic API: ``Pool.map`` with a chunksize to reduce inter-process traffic."""
    with mp.get_context().Pool(workers) as pool:
        return pool.map(bright_pixels, tiles, chunksize=2)


def _count_slice(name: str, start: int, stop: int, threshold: int) -> int:
    existing = shared_memory.SharedMemory(name=name)  # attach, don't copy
    try:
        data = existing.buf
        assert data is not None
        return sum(1 for pixel in bytes(data[start:stop]) if pixel >= threshold)
    finally:
        existing.close()


def bright_pixels_shared(tile: bytes, parts: int = 4, threshold: int = 200) -> int:
    """Put the tile in shared memory once; each process reads its own slice by name."""
    block = shared_memory.SharedMemory(create=True, size=len(tile))
    try:
        assert block.buf is not None
        block.buf[: len(tile)] = tile
        step = -(-len(tile) // parts)
        bounds = [(i, min(i + step, len(tile))) for i in range(0, len(tile), step)]
        with ProcessPoolExecutor(max_workers=parts) as pool:
            counts = pool.map(_count_slice, [block.name] * len(bounds), *zip(*bounds, strict=True),
                              [threshold] * len(bounds))
            return sum(counts)
    finally:
        block.close()
        block.unlink()  # free the OS resource – otherwise it leaks until reboot


def _add_bright(counter: object, tile: bytes, threshold: int) -> None:
    found = bright_pixels(tile, threshold)
    with counter.get_lock():  # type: ignore[attr-defined]
        counter.value += found  # type: ignore[attr-defined]


def count_with_shared_value(tiles: list[bytes], threshold: int = 200) -> int:
    """A ``Value`` lives in shared memory; its lock prevents lost updates across processes."""
    ctx = mp.get_context()
    counter = ctx.Value("q", 0)
    workers = [ctx.Process(target=_add_bright, args=(counter, tile, threshold)) for tile in tiles]
    for worker in workers:
        worker.start()
    for worker in workers:
        worker.join()
        if worker.exitcode != 0:
            raise RuntimeError(f"worker failed with exit code {worker.exitcode}")
    return int(counter.value)


@dataclass(frozen=True, slots=True)
class Workload:
    cpu_bound: bool
    task_seconds: float
    data_mb: float


def choose_executor(work: Workload) -> str:
    """Rule of thumb for picking a concurrency model."""
    if not work.cpu_bound:
        return "threads (or asyncio): the work waits on I/O, so the GIL is released"
    if work.task_seconds < 0.01:
        return "single process: tasks are too small to pay process start-up and pickling costs"
    if work.data_mb > 100:
        return "processes + shared memory: avoid pickling large inputs to every worker"
    return "process pool: CPU-bound pure Python needs separate interpreters to use all cores"


def benchmark(tiles: list[bytes], runner: Callable[[list[bytes]], list[int]]) -> dict[str, float]:
    start = time.perf_counter()
    sequential = [bright_pixels(t) for t in tiles]
    seq_time = time.perf_counter() - start
    start = time.perf_counter()
    parallel = runner(tiles)
    par_time = time.perf_counter() - start
    if parallel != sequential:
        raise AssertionError("parallel result differs from sequential")
    return {"sequential_s": round(seq_time, 3), "parallel_s": round(par_time, 3),
            "speedup": round(seq_time / par_time, 2), "cpus": float(os.cpu_count() or 1)}


def main() -> None:
    print("Day 74 – Satellite tile analysis\n")
    tiles = [make_tile(seed) for seed in range(1, 7)]
    print("bright pixels per tile:", analyse_tiles(tiles))
    print("Pool.map gives the same:", analyse_tiles_pool(tiles) == analyse_tiles(tiles))
    print("shared-memory count for tile 0:", bright_pixels_shared(tiles[0]), "=", bright_pixels(tiles[0]))
    print("shared Value total:", count_with_shared_value(tiles[:3]))
    print("benchmark:", benchmark(tiles, analyse_tiles))
    for work in (Workload(False, 1, 1), Workload(True, 0.001, 1), Workload(True, 2, 500), Workload(True, 2, 5)):
        print(f"  {work} → {choose_executor(work)}")


if __name__ == "__main__":
    main()
