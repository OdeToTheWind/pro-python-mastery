"""Day 73 – Concurrency: Threading.

Scenario: a *photo-sharing upload service*. Thumbnails are fetched from slow
storage (I/O bound → threads help), view counters are updated from many
threads (needs a lock), and uploads flow through a producer/consumer queue.
A CPU-bound resize shows why the GIL limits threads for pure-Python work.

Deliverables (syllabus):
* ``threading`` (Thread, ThreadPoolExecutor, Event)
* Locks (race conditions and how a Lock prevents them)
* Queues (thread-safe producer/consumer with sentinels)
* GIL implications (I/O-bound speeds up, CPU-bound does not)
"""

from __future__ import annotations

import queue
import sys
import threading
import time
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field

DELIVERABLES: dict[str, str] = {
    "threading.Thread": "upload_pipeline",
    "ThreadPoolExecutor": "fetch_thumbnails",
    "race condition": "ViewCounter.unsafe_increment",
    "Lock": "ViewCounter.safe_increment",
    "queue.Queue producer/consumer": "upload_pipeline",
    "threading.Event for shutdown": "Heartbeat",
    "GIL implications: I/O vs CPU": "gil_experiment",
}


def fetch_thumbnail(photo_id: int, latency: float = 0.05) -> str:
    """Simulated network/storage call: ``time.sleep`` releases the GIL like real I/O."""
    time.sleep(latency)
    return f"thumb-{photo_id}.jpg"


def fetch_thumbnails(ids: list[int], workers: int = 8, latency: float = 0.05) -> tuple[list[str], float]:
    """Fetch concurrently; ``map`` keeps the results in input order."""
    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=workers) as pool:
        results = list(pool.map(lambda i: fetch_thumbnail(i, latency), ids))
    return results, time.perf_counter() - start


@dataclass
class ViewCounter:
    views: int = 0
    lock: threading.Lock = field(default_factory=threading.Lock)

    def unsafe_increment(self) -> None:
        current = self.views  # read
        time.sleep(0)  # yield to another thread between read and write
        self.views = current + 1  # write – may overwrite another thread's update

    def safe_increment(self) -> None:
        with self.lock:  # only one thread inside at a time
            current = self.views
            time.sleep(0)
            self.views = current + 1


def hammer(increment: Callable[[], None], threads: int = 8, per_thread: int = 200) -> None:
    def work() -> None:
        for _ in range(per_thread):
            increment()

    workers = [threading.Thread(target=work) for _ in range(threads)]
    for worker in workers:
        worker.start()
    for worker in workers:
        worker.join()


_SENTINEL = object()


def upload_pipeline(files: list[str], consumers: int = 3) -> tuple[list[str], list[str]]:
    """One producer puts work on a ``Queue``; consumers process until they get a sentinel."""
    jobs: queue.Queue[object] = queue.Queue(maxsize=4)  # bounded → back-pressure on the producer
    done: list[str] = []
    errors: list[str] = []
    done_lock = threading.Lock()

    def consumer() -> None:
        while True:
            item = jobs.get()
            try:
                if item is _SENTINEL:
                    return
                name = str(item)
                if not name.endswith((".jpg", ".png")):
                    raise ValueError(f"unsupported file {name}")
                with done_lock:
                    done.append(name.upper())
            except ValueError as exc:
                with done_lock:
                    errors.append(str(exc))
            finally:
                jobs.task_done()

    workers = [threading.Thread(target=consumer, daemon=True) for _ in range(consumers)]
    for worker in workers:
        worker.start()
    for name in files:
        jobs.put(name)
    for _ in workers:
        jobs.put(_SENTINEL)
    jobs.join()
    return sorted(done), sorted(errors)


class Heartbeat(threading.Thread):
    """A background thread stopped cleanly with an ``Event`` instead of being killed."""

    def __init__(self, interval: float) -> None:
        super().__init__(daemon=True)
        self.interval = interval
        self.beats = 0
        self.stop_event = threading.Event()

    def run(self) -> None:
        while not self.stop_event.wait(self.interval):
            self.beats += 1

    def stop(self) -> None:
        self.stop_event.set()
        self.join()


def cpu_work(n: int) -> int:
    return sum(i * i % 7 for i in range(n))


def gil_experiment(tasks: int = 4, n: int = 200_000, latency: float = 0.05) -> dict[str, float]:
    """Speed-up of 4 threads vs sequential, for I/O-bound and CPU-bound work."""

    def timed(func: Callable[[], object]) -> float:
        start = time.perf_counter()
        func()
        return time.perf_counter() - start

    def threaded(target: Callable[[], object]) -> None:
        with ThreadPoolExecutor(tasks) as pool:
            for future in [pool.submit(target) for _ in range(tasks)]:
                future.result()

    io_seq = timed(lambda: [fetch_thumbnail(0, latency) for _ in range(tasks)])
    io_par = timed(lambda: threaded(lambda: fetch_thumbnail(0, latency)))
    cpu_seq = timed(lambda: [cpu_work(n) for _ in range(tasks)])
    cpu_par = timed(lambda: threaded(lambda: cpu_work(n)))
    return {"io_speedup": round(io_seq / io_par, 2), "cpu_speedup": round(cpu_seq / cpu_par, 2),
            "gil_enabled": float(getattr(sys, "_is_gil_enabled", lambda: True)())}


def main() -> None:
    print("Day 73 – Photo service threads\n")
    thumbs, seconds = fetch_thumbnails(list(range(16)))
    print(f"16 thumbnails in {seconds:.2f}s (sequential would take ~0.80s): {thumbs[:3]}…")
    unsafe, safe = ViewCounter(), ViewCounter()
    hammer(unsafe.unsafe_increment)
    hammer(safe.safe_increment)
    print(f"views expected 1600 → unsafe {unsafe.views}, with Lock {safe.views}")
    print("pipeline:", upload_pipeline(["a.jpg", "b.png", "notes.txt", "c.jpg"]))
    beat = Heartbeat(0.01)
    beat.start()
    time.sleep(0.05)
    beat.stop()
    print("heartbeats before clean stop:", beat.beats)
    print("GIL experiment:", gil_experiment())


if __name__ == "__main__":
    main()
