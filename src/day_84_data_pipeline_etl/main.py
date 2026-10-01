"""Day 84 – Capstone: Data Pipeline / ETL Script.

Scenario: a *city air-quality ETL*. Sensor stations drop CSV and JSON-lines
files into an inbox folder; the pipeline extracts records lazily, transforms
and validates them, quarantines bad rows with reasons, loads clean data into
JSON-lines output, and writes a run summary – logging every step.

Deliverables (syllabus):
* Generators (streaming extract → transform → load)
* ``pathlib`` (discovering, reading and writing files)
* CSV / JSON (both formats in, JSON-lines and JSON summary out)
* Error handling (bad files and bad rows never stop the run)
* Logging (per-stage counts and warnings)
"""

from __future__ import annotations

import csv
import json
import logging
from collections import Counter, defaultdict
from collections.abc import Iterable, Iterator
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

DELIVERABLES: dict[str, str] = {
    "extract: discover files with pathlib": "discover",
    "extract: stream CSV and JSON-lines": "extract",
    "transform: normalise and validate": "transform",
    "quarantine bad rows with reasons": "RunStats",
    "load: write JSON-lines": "load",
    "summary report": "summarise",
    "orchestration + logging": "run_pipeline",
}

log = logging.getLogger("airq.etl")
LIMITS = {"pm25": (0.0, 1000.0), "no2": (0.0, 2000.0)}


@dataclass(frozen=True, slots=True)
class Reading:
    station: str
    timestamp: str
    pm25: float
    no2: float


@dataclass
class RunStats:
    files: int = 0
    bad_files: list[str] = field(default_factory=list)
    extracted: int = 0
    loaded: int = 0
    rejected: Counter[str] = field(default_factory=Counter)
    quarantine: list[dict[str, Any]] = field(default_factory=list)


def discover(inbox: Path) -> list[Path]:
    """Sorted for reproducible runs; hidden/temp files are ignored."""
    return sorted(p for p in inbox.glob("*") if p.suffix in {".csv", ".jsonl"} and not p.name.startswith("."))


def extract(paths: Iterable[Path], stats: RunStats) -> Iterator[tuple[str, dict[str, Any]]]:
    """Yield (source, raw record) one at a time – files are never loaded fully."""
    for path in paths:
        stats.files += 1
        try:
            with path.open(encoding="utf-8", newline="") as handle:
                if path.suffix == ".csv":
                    for row in csv.DictReader(handle):
                        stats.extracted += 1
                        yield path.name, dict(row)
                else:
                    for number, line in enumerate(handle, start=1):
                        if not line.strip():
                            continue
                        stats.extracted += 1
                        try:
                            yield path.name, json.loads(line)
                        except json.JSONDecodeError as exc:
                            stats.rejected["invalid json"] += 1
                            stats.quarantine.append({"source": f"{path.name}:{number}", "reason": f"invalid json: {exc.msg}"})
        except (OSError, UnicodeDecodeError, csv.Error) as exc:
            log.warning("skipping unreadable file %s: %s", path.name, exc)
            stats.bad_files.append(path.name)


def _parse_time(value: str) -> str:
    for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M", "%d/%m/%Y %H:%M"):
        try:
            return datetime.strptime(value.strip(), fmt).strftime("%Y-%m-%dT%H:%M")
        except ValueError:
            continue
    raise ValueError(f"unrecognised timestamp {value!r}")


def transform(records: Iterable[tuple[str, dict[str, Any]]], stats: RunStats) -> Iterator[Reading]:
    seen: set[tuple[str, str]] = set()
    for source, raw in records:
        try:
            station = str(raw.get("station") or "").strip().upper()
            if not station:
                raise ValueError("missing station")
            reading = Reading(station, _parse_time(str(raw.get("timestamp", ""))),
                              float(raw.get("pm25", "nan")), float(raw.get("no2", "nan")))
            for name, (low, high) in LIMITS.items():
                value = getattr(reading, name)
                if not low <= value <= high:  # also rejects NaN
                    raise ValueError(f"{name} out of range")
            key = (reading.station, reading.timestamp)
            if key in seen:
                raise ValueError("duplicate reading")
            seen.add(key)
        except (ValueError, TypeError) as exc:
            reason = str(exc).split(" '")[0]
            stats.rejected[reason] += 1
            stats.quarantine.append({"source": source, "reason": str(exc), "record": raw})
            continue
        yield reading


def load(readings: Iterable[Reading], out_file: Path, stats: RunStats) -> None:
    out_file.parent.mkdir(parents=True, exist_ok=True)
    tmp = out_file.with_suffix(".tmp")
    with tmp.open("w", encoding="utf-8") as handle:
        for reading in readings:
            handle.write(json.dumps(asdict(reading)) + "\n")
            stats.loaded += 1
    tmp.replace(out_file)  # consumers never see a half-written file


def summarise(out_file: Path) -> dict[str, dict[str, float]]:
    totals: dict[str, list[float]] = defaultdict(list)
    with out_file.open(encoding="utf-8") as handle:
        for line in handle:
            row = json.loads(line)
            totals[row["station"]].append(row["pm25"])
    return {s: {"readings": len(v), "avg_pm25": round(sum(v) / len(v), 1), "max_pm25": max(v)}
            for s, v in sorted(totals.items())}


def run_pipeline(inbox: Path, outbox: Path) -> RunStats:
    stats = RunStats()
    files = discover(inbox)
    log.info("found %d input files", len(files))
    out_file = outbox / "readings.jsonl"
    load(transform(extract(files, stats), stats), out_file, stats)  # one streaming pass
    report = {"stats": {"files": stats.files, "bad_files": stats.bad_files, "extracted": stats.extracted,
                        "loaded": stats.loaded, "rejected": dict(stats.rejected)},
              "stations": summarise(out_file)}
    (outbox / "summary.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    (outbox / "quarantine.jsonl").write_text("".join(json.dumps(q) + "\n" for q in stats.quarantine),
                                             encoding="utf-8")
    log.info("loaded %d / %d records, rejected %d", stats.loaded, stats.extracted, sum(stats.rejected.values()))
    return stats


def seed_inbox(inbox: Path) -> None:
    inbox.mkdir(parents=True, exist_ok=True)
    (inbox / "north.csv").write_text(
        "station,timestamp,pm25,no2\nnorth,2026-10-01T08:00:00,12.5,40\nnorth,2026-10-01T09:00:00,15.0,38\n"
        "north,2026-10-01T09:00:00,15.0,38\n,2026-10-01T10:00:00,1,1\nnorth,yesterday,1,1\n", encoding="utf-8")
    (inbox / "south.jsonl").write_text(
        '{"station": "south", "timestamp": "01/10/2026 08:00", "pm25": 30.1, "no2": 55}\n'
        '{"station": "south", "timestamp": "2026-10-01 09:00", "pm25": -4, "no2": 50}\n'
        "{broken json\n", encoding="utf-8")
    (inbox / "legacy.csv").write_bytes(b"station,timestamp\n\xff\xfe broken encoding\n")
    (inbox / "notes.txt").write_text("not data", encoding="utf-8")


def main() -> None:
    import tempfile

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    print("Day 84 – Air-quality ETL\n")
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        seed_inbox(root / "inbox")
        stats = run_pipeline(root / "inbox", root / "out")
        print(json.dumps(json.loads((root / "out" / "summary.json").read_text()), indent=2))
        print("quarantined:", len(stats.quarantine))


if __name__ == "__main__":
    main()
