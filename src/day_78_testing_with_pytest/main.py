"""Day 78 – Testing with pytest.

Scenario: a *parcel-shipping quote service* that calls a carrier's rate API.
This module is the code under test; ``tests/test_day_78.py`` is the real
lesson – it shows fixtures (scopes, factories, teardown, built-ins),
parametrisation (ids, stacked parameters), mocking (``Mock(spec=...)``,
``patch``, ``monkeypatch``, call assertions) and coverage.

Deliverables (syllabus):
* Fixtures
* Parametrisation
* Mocking
* Coverage (measured programmatically with ``coverage``'s API)
"""

from __future__ import annotations

import time
from collections.abc import Callable
from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal
from typing import Any, Protocol

DELIVERABLES: dict[str, str] = {
    "code under test with an injectable dependency": "QuoteService",
    "factory used by fixtures": "make_parcel",
    "fake carrier (test double)": "FakeCarrier",
    "table used for parametrisation": "ZONE_CASES",
    "time source to monkeypatch": "QuoteService.quote",
    "coverage measured programmatically": "measure_coverage",
}


class CarrierError(Exception):
    pass


class Carrier(Protocol):
    def base_rate(self, origin: str, destination: str, weight_kg: float) -> Decimal: ...


@dataclass(frozen=True, slots=True)
class Parcel:
    weight_kg: float
    length_cm: int
    width_cm: int
    height_cm: int
    origin: str = "DE"
    destination: str = "DE"
    express: bool = False

    @property
    def volumetric_kg(self) -> float:
        return round(self.length_cm * self.width_cm * self.height_cm / 5000, 2)

    @property
    def chargeable_kg(self) -> float:
        return max(self.weight_kg, self.volumetric_kg)


def make_parcel(**overrides: Any) -> Parcel:
    """Sensible defaults + overrides – the shape of a good 'factory fixture'."""
    data: dict[str, Any] = {"weight_kg": 2.0, "length_cm": 30, "width_cm": 20, "height_cm": 10, **overrides}
    return Parcel(**data)


EU = {"DE", "FR", "NL", "IT", "ES"}
ZONE_CASES: list[tuple[str, str, str]] = [
    ("DE", "DE", "domestic"),
    ("DE", "FR", "eu"),
    ("FR", "IT", "eu"),
    ("DE", "US", "world"),
    ("IN", "DE", "world"),
]
ZONE_SURCHARGE = {"domestic": Decimal("0"), "eu": Decimal("4.50"), "world": Decimal("19.00")}


def zone(origin: str, destination: str) -> str:
    if origin == destination:
        return "domestic"
    return "eu" if {origin, destination} <= EU else "world"


class QuoteService:
    MAX_KG = 31.5

    def __init__(self, carrier: Carrier, clock: Callable[[], float] = time.time) -> None:
        self.carrier = carrier
        self.clock = clock
        self._cache: dict[tuple[str, str, float], tuple[float, Decimal]] = {}

    def quote(self, parcel: Parcel, ttl_seconds: float = 60) -> Decimal:
        if parcel.weight_kg <= 0:
            raise ValueError("weight must be positive")
        if parcel.chargeable_kg > self.MAX_KG:
            raise ValueError(f"parcel exceeds {self.MAX_KG} kg")
        key = (parcel.origin, parcel.destination, parcel.chargeable_kg)
        cached = self._cache.get(key)
        now = self.clock()
        if cached and now - cached[0] < ttl_seconds:
            base = cached[1]
        else:
            try:
                base = self.carrier.base_rate(parcel.origin, parcel.destination, parcel.chargeable_kg)
            except TimeoutError as exc:
                raise CarrierError("carrier did not respond") from exc
            self._cache[key] = (now, base)
        price = base + ZONE_SURCHARGE[zone(parcel.origin, parcel.destination)]
        if parcel.express:
            price *= Decimal("1.5")
        return price.quantize(Decimal("0.01"), ROUND_HALF_UP)


class FakeCarrier:
    """A hand-written fake: real behaviour, no network, records its calls."""

    def __init__(self, per_kg: Decimal = Decimal("1.20"), fail: bool = False) -> None:
        self.per_kg, self.fail = per_kg, fail
        self.calls: list[tuple[str, str, float]] = []

    def base_rate(self, origin: str, destination: str, weight_kg: float) -> Decimal:
        self.calls.append((origin, destination, weight_kg))
        if self.fail:
            raise TimeoutError
        return Decimal("3.99") + self.per_kg * Decimal(str(weight_kg))


def measure_coverage(func: Callable[[], object]) -> dict[str, Any]:
    """Run *func* under ``coverage`` and report which lines of this module executed."""
    import coverage

    # config_file=False: ignore the repo's [tool.coverage] settings and measure only this file
    cov = coverage.Coverage(include=[__file__], data_file=None, branch=True, config_file=False)
    cov.start()
    try:
        func()
    finally:
        cov.stop()
    _, statements, _, missing, _ = cov.analysis2(__file__)
    return {"statements": len(statements), "missing": len(missing),
            "percent": round(100 * (len(statements) - len(missing)) / len(statements), 1)}


def main() -> None:
    service = QuoteService(FakeCarrier())
    print("Day 78 – Shipping quotes (see tests/test_day_78.py for the pytest lesson)\n")
    for origin, destination, expected in ZONE_CASES:
        parcel = make_parcel(origin=origin, destination=destination)
        print(f"{origin}→{destination} ({expected:<8}) €{service.quote(parcel)}")
    print("express heavy box: €", service.quote(make_parcel(weight_kg=20, express=True)))
    print("coverage of one quote call:", measure_coverage(lambda: QuoteService(FakeCarrier()).quote(make_parcel())))
    print("run the lesson: pytest tests/test_day_78.py -v --cov=src.day_78_testing_with_pytest --cov-report=term-missing")


if __name__ == "__main__":
    main()
