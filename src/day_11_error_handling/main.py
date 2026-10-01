"""Day 11 – Error Handling.

Scenario: a *greenhouse sensor log reader* – log files are messy, devices
disappear and humans type bad values. The program must keep going.

Deliverables (syllabus):
* ``try / except / else / finally``
* Common built-in exceptions
* Robust user-input handling
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path

DELIVERABLES: dict[str, str] = {
    "try/except/else/finally": "load_readings",
    "common exceptions": "provoke",
    "robust user input": "ask_float",
    "graceful recovery from bad data": "parse_line",
}


@dataclass
class LoadReport:
    readings: dict[str, float] = field(default_factory=dict)
    skipped: list[str] = field(default_factory=list)
    events: list[str] = field(default_factory=list)


def parse_line(line: str) -> tuple[str, float]:
    """Parse ``"sensor_id,temperature"``. Raises ``ValueError`` on bad lines."""
    sensor, value = line.split(",")  # ValueError if not exactly two fields
    temperature = float(value)  # ValueError if not numeric
    if not sensor.strip():
        raise ValueError("missing sensor id")
    return sensor.strip(), temperature


def load_readings(path: Path) -> LoadReport:
    """Read a sensor log showing every part of ``try/except/else/finally``."""
    report = LoadReport()
    try:
        handle = path.open(encoding="utf-8")
    except FileNotFoundError:
        report.events.append("except: file missing")
        return report
    else:
        report.events.append("else: file opened")
        try:
            for number, line in enumerate(handle, start=1):
                if not line.strip():
                    continue
                try:
                    sensor, temperature = parse_line(line.strip())
                except ValueError as exc:
                    report.skipped.append(f"line {number}: {exc}")
                else:
                    report.readings[sensor] = temperature
        finally:
            handle.close()
            report.events.append("finally: file closed")
    return report


def average(readings: dict[str, float]) -> float | None:
    try:
        return sum(readings.values()) / len(readings)
    except ZeroDivisionError:
        return None


def provoke(kind: str) -> str:
    """Trigger a common exception on purpose and return its class name."""
    actions: dict[str, Callable[[], object]] = {
        "ValueError": lambda: int("twelve"),
        "TypeError": lambda: "5" + 5,  # type: ignore[operator]
        "ZeroDivisionError": lambda: 1 / 0,
        "IndexError": lambda: [][0],
        "KeyError": lambda: dict[str, int]()["missing"],
        "AttributeError": lambda: None.upper(),  # type: ignore[attr-defined]
        "FileNotFoundError": lambda: Path("no/such/file.log").read_text(),
    }
    action = actions.get(kind)
    if action is None:
        raise ValueError(f"no demo for {kind!r}")
    try:
        action()
    except Exception as exc:  # noqa: BLE001 – the demo reports any class
        return type(exc).__name__
    return "no error"


def ask_float(prompt: str, ask: Callable[[str], str], attempts: int = 3) -> float | None:
    """Ask until a number is typed; ``None`` after too many tries or on EOF."""
    for _ in range(attempts):
        try:
            return float(ask(prompt))
        except ValueError:
            print("  ✗ please type a number such as 21.5")
        except EOFError:
            return None
    return None


def main(ask: Callable[[str], str] | None = None) -> None:
    import tempfile

    ask = ask or input
    print("Day 11 – Greenhouse sensor log reader\n")
    with tempfile.TemporaryDirectory() as tmp:
        log = Path(tmp) / "sensors.log"
        log.write_text("north,21.5\nsouth,abc\n\neast,19\nbroken line\n", encoding="utf-8")
        report = load_readings(log)
        print("events:", report.events)
        print("readings:", report.readings, "average:", average(report.readings))
        print("skipped:", report.skipped)
        print("missing file:", load_readings(Path(tmp) / "nope.log").events)
    for kind in ["ValueError", "TypeError", "IndexError", "KeyError", "ZeroDivisionError"]:
        print(f"  provoke({kind!r}) → {provoke(kind)}")
    value = ask_float("Manual reading for 'west': ", ask)
    print("west =", value if value is not None else "not recorded")


if __name__ == "__main__":
    main()
