"""Day 89 – Capstone: Background Task Runner.

Scenario: a *home-lab backup scheduler*. A small daemon reads job specs such
as ``"every 15 minutes"`` or ``"daily at 02:30"``, runs each job as a child
process with a timeout, never runs two copies of the same job at once,
refuses to start twice (PID file) and shuts down gracefully on SIGTERM.

Deliverables (syllabus):
* Scheduling with the ``schedule`` library (parsed human-friendly specs)
* Process management (``subprocess`` with timeouts, terminate → kill)
* Single-instance PID file with stale-lock recovery
* Graceful shutdown (signal handler + ``threading.Event``) and overlap protection
"""

from __future__ import annotations

import os
import re
import signal
import subprocess
import sys
import threading
import time
from collections.abc import Callable, Iterator, Sequence
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path
from types import FrameType

import schedule

DELIVERABLES: dict[str, str] = {
    "parse schedule specs": "parse_spec",
    "register jobs with schedule": "TaskRunner.add",
    "run child processes with timeouts": "run_command",
    "stop long-running workers": "stop_process",
    "single-instance PID file": "pid_file",
    "graceful shutdown on signals": "TaskRunner.install_signal_handlers",
    "main loop": "TaskRunner.run",
}

SPEC_RE = re.compile(
    r"^every (?:(?P<n>\d+) )?(?P<unit>second|minute|hour|day)s?(?: at (?P<at>\d{2}:\d{2}))?$"
    r"|^daily at (?P<daily>\d{2}:\d{2})$")


@dataclass
class JobResult:
    name: str
    returncode: int | None
    output: str
    seconds: float
    timed_out: bool = False

    @property
    def ok(self) -> bool:
        return self.returncode == 0 and not self.timed_out


def parse_spec(spec: str, scheduler: schedule.Scheduler) -> schedule.Job:
    """``"every 15 minutes"``, ``"every hour"``, ``"every day at 02:30"``, ``"daily at 02:30"``."""
    match = SPEC_RE.match(spec.strip().lower())
    if not match:
        raise ValueError(f"cannot understand schedule {spec!r}")
    if match["daily"]:
        return scheduler.every().day.at(match["daily"])
    job = getattr(scheduler.every(int(match["n"] or 1)), match["unit"] + "s")
    if match["at"]:
        if match["unit"] != "day":
            raise ValueError("'at HH:MM' only works with days")
        job = job.at(match["at"])
    return job


def run_command(name: str, argv: Sequence[str], timeout: float) -> JobResult:
    """``subprocess.run`` kills the child on timeout; we never use ``shell=True``."""
    start = time.perf_counter()
    try:
        done = subprocess.run(list(argv), capture_output=True, text=True, timeout=timeout, check=False)
    except subprocess.TimeoutExpired as exc:
        out = exc.stdout.decode() if isinstance(exc.stdout, bytes) else (exc.stdout or "")
        return JobResult(name, None, out, time.perf_counter() - start, timed_out=True)
    except OSError as exc:
        return JobResult(name, 127, str(exc), time.perf_counter() - start)
    return JobResult(name, done.returncode, (done.stdout + done.stderr).strip(), time.perf_counter() - start)


def stop_process(proc: subprocess.Popen[str], grace: float = 2.0) -> int:
    """Ask nicely (SIGTERM), wait, then insist (SIGKILL). Returns the exit code.

    On Windows both steps are ``TerminateProcess`` – there is no polite signal to ignore.
    """
    if proc.poll() is None:
        proc.terminate()
        try:
            return proc.wait(timeout=grace)
        except subprocess.TimeoutExpired:
            proc.kill()
    return proc.wait()


def _pid_alive(pid: int) -> bool:
    """Is ``pid`` running? On Windows ``os.kill(pid, 0)`` would send Ctrl+C, so ask the OS instead."""
    if sys.platform == "win32":  # pragma: no cover - exercised on Windows only
        return _windows_pid_alive(pid)
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:  # pragma: no cover - exists but owned by someone else
        return True
    return True


def _windows_pid_alive(pid: int) -> bool:  # pragma: no cover - Windows only
    import ctypes

    kernel32 = ctypes.windll.kernel32  # type: ignore[attr-defined]
    handle = kernel32.OpenProcess(0x1000, False, pid)  # PROCESS_QUERY_LIMITED_INFORMATION
    if not handle:
        return kernel32.GetLastError() == 5  # ERROR_ACCESS_DENIED: exists, owned by someone else
    try:
        code = ctypes.c_ulong()
        kernel32.GetExitCodeProcess(handle, ctypes.byref(code))
        return code.value == 259  # STILL_ACTIVE
    finally:
        kernel32.CloseHandle(handle)


@contextmanager
def pid_file(path: Path) -> Iterator[int]:
    """Atomic ``O_EXCL`` create: two runners can never both win the race."""
    path.parent.mkdir(parents=True, exist_ok=True)
    for _attempt in range(2):
        try:
            fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
            break
        except FileExistsError:
            text = path.read_text(encoding="utf-8").strip()
            if text.isdigit() and _pid_alive(int(text)):
                raise RuntimeError(f"already running as pid {text}") from None
            path.unlink(missing_ok=True)  # stale lock from a crashed runner
    else:  # pragma: no cover - lost a race twice
        raise RuntimeError("could not acquire pid file")
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        handle.write(str(os.getpid()))
    try:
        yield os.getpid()
    finally:
        path.unlink(missing_ok=True)


@dataclass
class TaskRunner:
    scheduler: schedule.Scheduler = field(default_factory=schedule.Scheduler)
    history: list[JobResult] = field(default_factory=list)
    stop_event: threading.Event = field(default_factory=threading.Event)
    running: set[str] = field(default_factory=set)
    skipped: list[str] = field(default_factory=list)
    _lock: threading.Lock = field(default_factory=threading.Lock)

    def add(self, name: str, spec: str, argv: Sequence[str], timeout: float = 60.0,
            background: bool = False) -> schedule.Job:
        def trigger() -> None:
            with self._lock:
                if name in self.running:  # previous run still busy → skip, don't pile up
                    self.skipped.append(name)
                    return
                self.running.add(name)
            if background:
                threading.Thread(target=self._execute, args=(name, argv, timeout), daemon=True).start()
            else:
                self._execute(name, argv, timeout)

        return parse_spec(spec, self.scheduler).do(trigger).tag(name)

    def _execute(self, name: str, argv: Sequence[str], timeout: float) -> None:
        try:
            result = run_command(name, argv, timeout)
            with self._lock:
                self.history.append(result)
        finally:
            with self._lock:
                self.running.discard(name)

    def install_signal_handlers(self) -> Callable[[], None]:
        """SIGTERM/SIGINT finish the current tick and exit; returns a function restoring old handlers."""

        def handler(signum: int, _frame: FrameType | None) -> None:
            self.stop_event.set()

        previous = {sig: signal.signal(sig, handler) for sig in (signal.SIGTERM, signal.SIGINT)}

        def restore() -> None:
            for sig, old in previous.items():
                signal.signal(sig, old)

        return restore

    def run(self, tick: float = 1.0, max_ticks: int | None = None) -> int:
        ticks = 0
        while not self.stop_event.is_set() and (max_ticks is None or ticks < max_ticks):
            self.scheduler.run_pending()
            ticks += 1
            self.stop_event.wait(tick)  # sleeps, but wakes instantly on shutdown
        return ticks


def main() -> None:
    import tempfile

    print("Day 89 – Home-lab backup scheduler\n")
    py = sys.executable
    runner = TaskRunner()
    runner.add("snapshot", "every 1 second", [py, "-c", "print('snapshot ok')"], timeout=5)
    runner.add("hung-sync", "every 1 second", [py, "-c", "import time; time.sleep(5)"], timeout=0.3)
    runner.add("offsite", "daily at 02:30", [py, "-c", "print('upload')"])
    for job in runner.scheduler.get_jobs():
        print(f"  {job!r}")
    with tempfile.TemporaryDirectory() as tmp, pid_file(Path(tmp) / "runner.pid") as pid:
        print("pid file holds", pid)
        restore = runner.install_signal_handlers()
        runner.scheduler.run_all()  # demo: force one round instead of waiting for the clock
        restore()
    for result in runner.history:
        state = "timeout" if result.timed_out else f"exit {result.returncode}"
        print(f"  {result.name:<10} {state:<8} {result.output!r}")


if __name__ == "__main__":
    main()
