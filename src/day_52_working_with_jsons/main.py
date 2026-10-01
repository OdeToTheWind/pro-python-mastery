"""Day 52 – Working with JSON.

Scenario: a *weather-station API client* that receives JSON payloads,
validates them into typed objects, and serialises its own reports – including
types JSON doesn't support natively (datetime, Decimal, dataclasses).

Deliverables (syllabus):
* JSON serialisation (``dumps``/``dump``, custom encoder, pretty vs compact)
* JSON parsing (``loads``/``load``, ``object_hook``, ``parse_float``)
* Payload handling (schema validation, clear errors, corrupt files)
"""

from __future__ import annotations

import contextlib
import dataclasses
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path
from typing import Any

DELIVERABLES: dict[str, str] = {
    "serialisation with a custom encoder": "to_json",
    "pretty vs compact output": "to_json",
    "parsing with object_hook / parse_float": "from_json",
    "payload validation": "parse_reading",
    "file save/load with corruption handling": "load_json",
}


class PayloadError(ValueError):
    """The payload is not valid JSON or does not match the expected schema."""


@dataclass(frozen=True, slots=True)
class Reading:
    station: str
    taken_at: datetime
    temperature_c: Decimal
    humidity: int


class ReportEncoder(json.JSONEncoder):
    """Teach ``json`` how to encode types it doesn't know."""

    def default(self, o: Any) -> Any:
        if isinstance(o, datetime):
            return o.isoformat()
        if isinstance(o, Decimal):
            return str(o)  # keep exact digits; a float would lose precision
        if dataclasses.is_dataclass(o) and not isinstance(o, type):
            return dataclasses.asdict(o)
        if isinstance(o, set | frozenset):
            return sorted(o)
        return super().default(o)


def to_json(data: Any, *, pretty: bool = True) -> str:
    if pretty:
        return json.dumps(data, cls=ReportEncoder, indent=2, ensure_ascii=False, sort_keys=True)
    return json.dumps(data, cls=ReportEncoder, separators=(",", ":"), ensure_ascii=False)


def _hook(obj: dict[str, Any]) -> dict[str, Any]:
    """``object_hook`` runs for every JSON object – revive ISO timestamps."""
    for key, value in obj.items():
        if key.endswith("_at") and isinstance(value, str):
            with contextlib.suppress(ValueError):  # not a timestamp after all – keep the string
                obj[key] = datetime.fromisoformat(value)
    return obj


def from_json(text: str | bytes) -> Any:
    """Parse JSON; floats become ``Decimal`` so 0.1 stays exactly 0.1."""
    try:
        return json.loads(text, object_hook=_hook, parse_float=Decimal)
    except json.JSONDecodeError as exc:
        raise PayloadError(f"invalid JSON at line {exc.lineno} col {exc.colno}: {exc.msg}") from exc


def parse_reading(payload: str | bytes) -> Reading:
    data = from_json(payload)
    if not isinstance(data, dict):
        raise PayloadError("payload must be a JSON object")
    required: dict[str, type | tuple[type, ...]] = {
        "station": str, "taken_at": datetime, "temperature_c": (Decimal, int), "humidity": int,
    }
    for key, kinds in required.items():
        if key not in data:
            raise PayloadError(f"missing field {key!r}")
        if not isinstance(data[key], kinds) or isinstance(data[key], bool):
            raise PayloadError(f"field {key!r} has the wrong type")
    if not 0 <= data["humidity"] <= 100:
        raise PayloadError("humidity must be 0–100")
    return Reading(data["station"], data["taken_at"], Decimal(data["temperature_c"]), data["humidity"])


def save_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(to_json(data) + "\n", encoding="utf-8")


def load_json(path: Path, default: Any = None) -> Any:
    """Missing file → *default*. Corrupt file → ``PayloadError`` (never a silent reset)."""
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return default
    return from_json(text)


SAMPLE_PAYLOAD = '{"station": "Reykjavík-01", "taken_at": "2026-05-03T06:00:00+00:00", "temperature_c": 4.1, "humidity": 87}'


def main() -> None:
    print("Day 52 – Weather station JSON\n")
    reading = parse_reading(SAMPLE_PAYLOAD)
    print("Parsed:", reading)
    report = {"generated_at": datetime(2026, 5, 3, 7, tzinfo=UTC), "readings": [reading],
              "stations": {"Reykjavík-01"}}
    print("Pretty:\n" + to_json(report))
    print("Compact:", to_json({"ok": True, "t": Decimal("4.1")}, pretty=False))
    for bad in ['{"station": "x"', '{"station": "x", "taken_at": "2026-01-01T00:00:00", "temperature_c": 1, "humidity": 140}']:
        try:
            parse_reading(bad)
        except PayloadError as exc:
            print("Rejected:", exc)


if __name__ == "__main__":
    main()
