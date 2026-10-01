"""Day 30 – Getting / Setting Attributes.

Scenario: a *smart thermostat* whose temperature can be read and written in
Celsius or Fahrenheit, but never set to an unsafe value.

Deliverables (syllabus):
* ``@property``
* Getters and setters (and a deleter)
* Controlled attribute access (validation, read-only and computed attributes,
  ``getattr``/``setattr``/``hasattr``)
"""

from __future__ import annotations

from typing import Any

DELIVERABLES: dict[str, str] = {
    "@property getter": "Thermostat.celsius",
    "setter with validation": "Thermostat.celsius",
    "computed property with setter": "Thermostat.fahrenheit",
    "read-only property": "Thermostat.history",
    "deleter": "Thermostat.schedule",
    "dynamic getattr/setattr/hasattr": "apply_settings",
}

MIN_C, MAX_C = 5.0, 30.0


class Thermostat:
    """Every write goes through the setter – including the one in ``__init__``."""

    def __init__(self, room: str, celsius: float = 20.0) -> None:
        self.room = room
        self._history: list[float] = []
        self._schedule: str | None = None
        self.celsius = celsius  # uses the setter, so bad values are rejected here too

    @property
    def celsius(self) -> float:
        return self._celsius

    @celsius.setter
    def celsius(self, value: float) -> None:
        if not isinstance(value, int | float) or isinstance(value, bool):
            raise TypeError("temperature must be a number")
        if not MIN_C <= value <= MAX_C:
            raise ValueError(f"temperature must be between {MIN_C} and {MAX_C} °C")
        self._celsius = float(value)
        self._history.append(self._celsius)

    @property
    def fahrenheit(self) -> float:
        """Computed from the stored Celsius value – never stored twice."""
        return round(self._celsius * 9 / 5 + 32, 1)

    @fahrenheit.setter
    def fahrenheit(self, value: float) -> None:
        self.celsius = round((value - 32) * 5 / 9, 1)

    @property
    def history(self) -> tuple[float, ...]:
        """Read-only: no setter, and a tuple so callers can't mutate our list."""
        return tuple(self._history)

    @property
    def schedule(self) -> str | None:
        return self._schedule

    @schedule.setter
    def schedule(self, value: str) -> None:
        self._schedule = value

    @schedule.deleter
    def schedule(self) -> None:
        self._schedule = None


def apply_settings(device: Thermostat, settings: dict[str, Any]) -> list[str]:
    """Apply settings by name using ``hasattr``/``setattr`` – the setters still validate."""
    errors = []
    for name, value in settings.items():
        if name.startswith("_") or not hasattr(device, name):
            errors.append(f"{name}: unknown setting")
            continue
        try:
            setattr(device, name, value)
        except (AttributeError, TypeError, ValueError) as exc:
            errors.append(f"{name}: {exc}")
    return errors


def main() -> None:
    print("Day 30 – Smart thermostat\n")
    living = Thermostat("living room")
    living.fahrenheit = 71.6
    unit = "fahrenheit"  # attribute name chosen at runtime
    print(f"{living.room}: {living.celsius} °C / {getattr(living, unit)} °F")
    print("Errors:", apply_settings(living, {"celsius": 45, "history": [], "colour": "red", "schedule": "eco"}))
    print("Schedule:", living.schedule)
    del living.schedule
    print("History (read-only):", living.history, "| schedule after del:", living.schedule)


if __name__ == "__main__":
    main()
