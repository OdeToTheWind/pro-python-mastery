"""Day 85 – Capstone: Concurrent File / Network Processor.

Scenario: a *podcast-archive mirroring tool*. Episodes are downloaded from a
feed server with asyncio (I/O bound, hundreds of sockets on one thread),
verified with SHA-256 in a thread pool (disk I/O releases the GIL), and
compressed for cold storage in a process pool (pure CPU work). One report
tells the operator what succeeded, what failed and why.

Deliverables (syllabus):
* Thread pools for blocking file I/O (``ThreadPoolExecutor`` + ``as_completed``)
* Process pools for CPU-bound work (``ProcessPoolExecutor``)
* asyncio for network I/O (``aiohttp``, semaphore limit, retries, timeouts)
* Picking the right tool per stage and collecting failures without stopping
"""

from __future__ import annotations

import asyncio
import hashlib
import multiprocessing
import os
import threading
import time
import zlib
from collections.abc import Awaitable, Callable, Iterable
from concurrent.futures import Executor, ProcessPoolExecutor, ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import aiohttp
from aiohttp import web
from aiohttp.test_utils import TestServer

DELIVERABLES: dict[str, str] = {
    "asyncio downloads with a concurrency limit": "download_all",
    "retries and timeouts per request": "download_one",
    "thread pool for file hashing": "checksum_files",
    "process pool for compression": "compress_files",
    "thread-safe progress counter": "Progress",
    "strategy per workload": "choose_executor",
    "end-to-end mirror run": "mirror",
}

CHUNK = 64 * 1024


@dataclass
class Result:
    name: str
    ok: bool
    detail: str = ""


@dataclass
class Report:
    downloaded: list[Result] = field(default_factory=list)
    hashes: dict[str, str] = field(default_factory=dict)
    compressed: dict[str, float] = field(default_factory=dict)
    failures: list[str] = field(default_factory=list)


class Progress:
    """Workers in many threads bump one counter – the lock keeps it exact."""

    def __init__(self, total: int) -> None:
        self.total = total
        self.done = 0
        self._lock = threading.Lock()

    def tick(self) -> int:
        with self._lock:
            self.done += 1
            return self.done

    @property
    def percent(self) -> float:
        return 100.0 * self.done / self.total if self.total else 100.0


def choose_executor(kind: str, workers: int = 4) -> Executor:
    """I/O-bound → threads (cheap, share memory); CPU-bound → processes (bypass the GIL)."""
    if kind == "io":
        return ThreadPoolExecutor(max_workers=workers, thread_name_prefix="io")
    if kind == "cpu":
        # "spawn" is safe even when threads are running (fork could deadlock) and matches Windows/macOS
        return ProcessPoolExecutor(max_workers=min(workers, os.cpu_count() or 1),
                                   mp_context=multiprocessing.get_context("spawn"))
    raise ValueError(f"unknown workload kind {kind!r} (use 'io' or 'cpu')")


async def download_one(session: aiohttp.ClientSession, url: str, dest: Path, *,
                       retries: int = 2, backoff: float = 0.01) -> Result:
    """Stream to a temp file, retry 5xx/timeouts with backoff, never leave partial files."""
    tmp = dest.with_suffix(dest.suffix + ".part")
    last = ""
    for attempt in range(retries + 1):
        try:
            async with session.get(url) as response:
                if response.status >= 500:
                    raise aiohttp.ClientResponseError(response.request_info, (), status=response.status)
                if response.status != 200:
                    return Result(dest.name, False, f"HTTP {response.status}")
                with tmp.open("wb") as handle:
                    async for chunk in response.content.iter_chunked(CHUNK):
                        handle.write(chunk)
            tmp.replace(dest)
            return Result(dest.name, True, f"{dest.stat().st_size} bytes")
        except (aiohttp.ClientError, TimeoutError) as exc:
            last = type(exc).__name__ if not isinstance(exc, aiohttp.ClientResponseError) else f"HTTP {exc.status}"
            tmp.unlink(missing_ok=True)
            await asyncio.sleep(backoff * 2**attempt)
    return Result(dest.name, False, f"gave up after {retries + 1} attempts: {last}")


async def download_all(base_url: str, names: Iterable[str], dest: Path, *, limit: int = 3,
                       timeout: float = 2.0, retries: int = 2) -> tuple[list[Result], int]:
    """Returns the results (in input order) and the peak number of requests in flight."""
    dest.mkdir(parents=True, exist_ok=True)
    gate = asyncio.Semaphore(limit)
    in_flight = peak = 0

    async def guarded(session: aiohttp.ClientSession, name: str) -> Result:
        nonlocal in_flight, peak
        async with gate:
            in_flight += 1
            peak = max(peak, in_flight)
            try:
                return await download_one(session, f"{base_url}/episodes/{name}", dest / name, retries=retries)
            finally:
                in_flight -= 1

    client_timeout = aiohttp.ClientTimeout(total=timeout)
    async with aiohttp.ClientSession(timeout=client_timeout) as session:
        results = await asyncio.gather(*(guarded(session, n) for n in names))
    return list(results), peak


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(CHUNK), b""):
            digest.update(block)
    return digest.hexdigest()


def checksum_files(paths: Iterable[Path], workers: int = 4,
                   progress: Progress | None = None) -> tuple[dict[str, str], list[str]]:
    hashes: dict[str, str] = {}
    errors: list[str] = []
    with choose_executor("io", workers) as pool:
        futures = {pool.submit(sha256_file, p): p for p in paths}
        for future in as_completed(futures):  # handle results as soon as each finishes
            path = futures[future]
            try:
                hashes[path.name] = future.result()
            except OSError as exc:
                errors.append(f"{path.name}: {exc.strerror or exc}")
            if progress:
                progress.tick()
    return dict(sorted(hashes.items())), errors


def compress_bytes(data: bytes) -> tuple[int, int]:
    """Top-level so it can be pickled into a worker process."""
    return len(data), len(zlib.compress(data, level=9))


def compress_files(paths: list[Path], workers: int = 2) -> dict[str, float]:
    """Return the compression ratio per file, computed in parallel processes."""
    with choose_executor("cpu", workers) as pool:
        sizes = pool.map(compress_bytes, (p.read_bytes() for p in paths))
        return {p.name: round(packed / raw, 3) if raw else 1.0 for p, (raw, packed) in zip(paths, sizes, strict=True)}


def mirror(base_url: str, names: list[str], dest: Path, *, limit: int = 3) -> Report:
    report = Report()
    report.downloaded, _peak = asyncio.run(download_all(base_url, names, dest, limit=limit))
    report.failures += [f"{r.name}: {r.detail}" for r in report.downloaded if not r.ok]
    files = [dest / r.name for r in report.downloaded if r.ok]
    report.hashes, errors = checksum_files(files, progress=Progress(len(files)))
    report.failures += errors
    report.compressed = compress_files(files)
    return report


# --- a local feed server for tests and the demo (no internet needed) --------
EPISODES = {f"ep{n:02d}.mp3": (f"episode {n} ".encode() * (200 * n)) for n in range(1, 6)}


def make_feed_app(*, delay: float = 0.0, flaky: set[str] | None = None) -> web.Application:
    remaining_failures = {name: 1 for name in flaky or set()}

    async def episode(request: web.Request) -> web.StreamResponse:
        name = request.match_info["name"]
        if delay:
            await asyncio.sleep(delay)
        if remaining_failures.get(name):
            remaining_failures[name] -= 1
            return web.Response(status=503)
        if name not in EPISODES:
            raise web.HTTPNotFound()
        return web.Response(body=EPISODES[name], content_type="audio/mpeg")

    app = web.Application()
    app.router.add_get("/episodes/{name}", episode)
    return app


async def with_feed_server(work: Callable[[str], Awaitable[Any]], **app_kwargs: Any) -> Any:
    async with TestServer(make_feed_app(**app_kwargs)) as server:
        return await work(str(server.make_url("")).rstrip("/"))


def main() -> None:
    import tempfile

    print("Day 85 – Podcast archive mirror\n")
    with tempfile.TemporaryDirectory() as tmp:
        names = [*EPISODES, "missing.mp3"]

        async def work(url: str) -> tuple[list[Result], int]:
            return await download_all(url, names, Path(tmp), limit=3)

        start = time.perf_counter()
        results, peak = asyncio.run(with_feed_server(work, delay=0.05, flaky={"ep02.mp3"}))
        print(f"downloaded in {time.perf_counter() - start:.2f}s, peak {peak} in flight")
        for r in results:
            print(f"  {'ok ' if r.ok else 'ERR'} {r.name:<12} {r.detail}")
        files = [Path(tmp) / r.name for r in results if r.ok]
        hashes, _ = checksum_files(files)
        print("sha256 ep01:", hashes["ep01.mp3"][:16], "…")
        print("compression ratios:", compress_files(files))


if __name__ == "__main__":
    main()
