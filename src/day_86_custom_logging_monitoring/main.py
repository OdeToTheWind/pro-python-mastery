"""Day 86 – Capstone: Custom Logging & Monitoring Tool.

Scenario: a *payment-gateway monitor*. Every payment attempt is logged as one
JSON object (with the request id carried by ``contextvars``), files rotate
before they fill the disk, latency and error counts are kept as metrics that
render in the Prometheus text format, and an alert handler pages the on-call
engineer when errors spike.

Deliverables (syllabus):
* Structured logging (JSON formatter, context filter, ``extra=`` fields)
* Log rotation (``RotatingFileHandler`` with size limit and backups)
* Basic metrics (counter, gauge, histogram percentiles, exposition text)
* Monitoring: a sliding-window alert handler and log-file analysis
"""

from __future__ import annotations

import contextvars
import json
import logging
import logging.handlers
import random
import time
from collections import Counter, deque
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

DELIVERABLES: dict[str, str] = {
    "JSON log formatter": "JsonFormatter",
    "request-id context filter": "RequestContextFilter",
    "rotating file handler setup": "configure_logging",
    "metrics registry": "Metrics",
    "histogram percentiles": "Histogram.percentile",
    "Prometheus text exposition": "Metrics.render",
    "error-spike alert handler": "AlertHandler",
    "log analysis": "analyse_log",
}

request_id: contextvars.ContextVar[str] = contextvars.ContextVar("request_id", default="-")
_STANDARD = set(vars(logging.makeLogRecord({}))) | {"message", "asctime", "request_id"}


class RequestContextFilter(logging.Filter):
    """Copies the current request id onto every record – no need to pass it around."""

    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = request_id.get()
        return True


@contextmanager
def request_context(rid: str) -> Iterator[None]:
    token = request_id.set(rid)
    try:
        yield
    finally:
        request_id.reset(token)


class JsonFormatter(logging.Formatter):
    """One JSON object per line: machine-searchable, safe against newlines in messages."""

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "ts": datetime.fromtimestamp(record.created, UTC).isoformat(timespec="milliseconds"),
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
            "request_id": getattr(record, "request_id", "-"),
        }
        payload.update({k: v for k, v in vars(record).items() if k not in _STANDARD})  # extra=
        if record.exc_info:
            payload["exc"] = self.formatException(record.exc_info)
        return json.dumps(payload, default=str)


class AlertHandler(logging.Handler):
    """Fires ``notify`` once when ``threshold`` errors happen within ``window`` seconds."""

    def __init__(self, notify: Callable[[str], None], threshold: int = 3, window: float = 60.0,
                 clock: Callable[[], float] = time.monotonic) -> None:
        super().__init__(level=logging.ERROR)
        self.notify, self.threshold, self.window, self.clock = notify, threshold, window, clock
        self.times: deque[float] = deque()
        self.firing = False

    def emit(self, record: logging.LogRecord) -> None:
        now = self.clock()
        self.times.append(now)
        while self.times and now - self.times[0] > self.window:
            self.times.popleft()
        if len(self.times) >= self.threshold and not self.firing:
            self.firing = True  # no alert storm: one page until it recovers
            self.notify(f"{len(self.times)} errors in {self.window:.0f}s, last: {record.getMessage()}")
        elif len(self.times) < self.threshold:
            self.firing = False


def configure_logging(log_file: Path, *, max_bytes: int = 1_000_000, backups: int = 3,
                      alert: AlertHandler | None = None) -> logging.Logger:
    log_file.parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("payments")
    for handler in logger.handlers:
        handler.close()
    rotating = logging.handlers.RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backups,
                                                    encoding="utf-8")
    rotating.setFormatter(JsonFormatter())
    rotating.addFilter(RequestContextFilter())
    logger.handlers = [rotating, *([alert] if alert else [])]
    logger.setLevel(logging.INFO)
    logger.propagate = False
    return logger


class Histogram:
    def __init__(self, buckets: tuple[float, ...] = (0.05, 0.1, 0.25, 0.5, 1.0)) -> None:
        self.buckets = buckets
        self.values: list[float] = []

    def observe(self, value: float) -> None:
        self.values.append(value)

    def percentile(self, p: float) -> float:
        """Nearest-rank percentile (p in 0–100)."""
        if not self.values:
            return 0.0
        ordered = sorted(self.values)
        rank = max(1, -(-len(ordered) * p // 100))  # ceil without floats drifting
        return ordered[int(rank) - 1]

    def bucket_counts(self) -> list[tuple[str, int]]:
        counts = [(str(b), sum(v <= b for v in self.values)) for b in self.buckets]
        return [*counts, ("+Inf", len(self.values))]


class Metrics:
    def __init__(self) -> None:
        self.counters: Counter[tuple[str, str]] = Counter()
        self.gauges: dict[str, float] = {}
        self.histograms: dict[str, Histogram] = {}

    def inc(self, name: str, label: str = "", amount: int = 1) -> None:
        self.counters[(name, label)] += amount

    def set_gauge(self, name: str, value: float) -> None:
        self.gauges[name] = value

    def observe(self, name: str, value: float) -> None:
        self.histograms.setdefault(name, Histogram()).observe(value)

    def render(self) -> str:
        lines = []
        for (name, label), value in sorted(self.counters.items()):
            lines.append(f'{name}{{status="{label}"}} {value}' if label else f"{name} {value}")
        lines += [f"{name} {value}" for name, value in sorted(self.gauges.items())]
        for name, hist in sorted(self.histograms.items()):
            lines += [f'{name}_bucket{{le="{le}"}} {count}' for le, count in hist.bucket_counts()]
            lines += [f"{name}_sum {sum(hist.values):.3f}", f"{name}_count {len(hist.values)}"]
        return "\n".join(lines) + "\n"


def process_payment(logger: logging.Logger, metrics: Metrics, amount_cents: int, *,
                    latency: float, declined: bool = False) -> bool:
    """A fake gateway call: log it, count it, time it."""
    metrics.observe("payment_latency_seconds", latency)
    if amount_cents <= 0:
        metrics.inc("payments_total", "error")
        logger.error("invalid amount", extra={"amount_cents": amount_cents})
        return False
    status = "declined" if declined else "approved"
    metrics.inc("payments_total", status)
    logger.info("payment %s", status, extra={"amount_cents": amount_cents, "latency_ms": round(latency * 1000)})
    return not declined


def analyse_log(log_dir: Path, stem: str = "payments.log") -> dict[str, Any]:
    """Read the current file *and* rotated backups, oldest first."""
    files = sorted(log_dir.glob(f"{stem}*"), key=lambda p: -int(p.suffix[1:]) if p.suffix[1:].isdigit() else 0)
    levels: Counter[str] = Counter()
    requests: set[str] = set()
    for path in files:
        for line in path.read_text(encoding="utf-8").splitlines():
            entry = json.loads(line)
            levels[entry["level"]] += 1
            requests.add(entry["request_id"])
    total = sum(levels.values())
    return {"files": len(files), "lines": total, "levels": dict(levels), "requests": len(requests),
            "error_rate": round(levels["ERROR"] / total, 3) if total else 0.0}


def main() -> None:
    import tempfile

    print("Day 86 – Payment-gateway monitor\n")
    rng = random.Random(86)
    with tempfile.TemporaryDirectory() as tmp:
        pages: list[str] = []
        logger = configure_logging(Path(tmp) / "payments.log", max_bytes=2_000, backups=2,
                                   alert=AlertHandler(pages.append, threshold=3))
        metrics = Metrics()
        for n in range(30):
            with request_context(f"req-{n:03d}"):
                amount = 0 if n in {20, 21, 22} else rng.randint(100, 9_000)
                process_payment(logger, metrics, amount, latency=rng.uniform(0.02, 0.6), declined=n % 7 == 0)
        metrics.set_gauge("gateway_up", 1)
        print(metrics.render())
        print("p95 latency:", round(metrics.histograms["payment_latency_seconds"].percentile(95), 3))
        print("pages:", pages)
        print("analysis:", analyse_log(Path(tmp)))
        for handler in logger.handlers:
            handler.close()


if __name__ == "__main__":
    main()
