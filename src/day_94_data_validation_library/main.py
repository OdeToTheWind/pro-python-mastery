"""Day 94 – Capstone: Data Validation & Cleaning Library.

Scenario: ``intake`` – a reusable validation library for a *clinical-trial
patient intake* system. Messy form data ("72,5 kg", " F ", "1980/03/07")
is cleaned and validated by small composable, type-hinted validators; every
error carries its exact path (``visits[1].date``) so a coordinator can fix
the whole form in one go.

Deliverables (syllabus):
* Reusable validators (generic ``Validator[T]``, composition with ``>>``,
  ``optional``, ``default``)
* Custom exceptions (``ValidationError`` with path, ``SchemaError`` aggregate)
* Type hints throughout (``Generic``, ``Callable``, ``Mapping``)
* Cleaning helpers and a batch report (clean rows vs rejected rows)
"""

from __future__ import annotations

import re
from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from typing import Any, Generic, TypeVar

T = TypeVar("T")
U = TypeVar("U")

DELIVERABLES: dict[str, str] = {
    "generic composable validator": "Validator",
    "string / number / date / choice validators": "text",
    "list and nested schema validators": "schema",
    "custom exception with field path": "ValidationError",
    "aggregated schema errors": "SchemaError",
    "cleaning helpers": "parse_measurement",
    "batch validation report": "validate_batch",
}


class ValidationError(ValueError):
    def __init__(self, message: str, path: str = "", value: Any = None) -> None:
        self.message, self.path, self.value = message, path, value
        super().__init__(f"{path}: {message}" if path else message)

    def at(self, segment: str) -> ValidationError:
        """Prefix the path while the error bubbles up through nested validators."""
        joined = segment + ("" if not self.path or self.path.startswith("[") else ".") + self.path
        return ValidationError(self.message, joined, self.value)


class SchemaError(ValidationError):
    def __init__(self, errors: list[ValidationError]) -> None:
        self.errors = errors
        super().__init__(f"{len(errors)} problem(s): " + "; ".join(str(e) for e in errors))

    def at(self, segment: str) -> SchemaError:
        return SchemaError([e.at(segment) for e in self.errors])


class Validator(Generic[T]):  # noqa: UP046 - Generic spelled out as the teaching point
    """Wraps ``Callable[[Any], T]``; ``a >> b`` feeds a's cleaned output into b."""

    def __init__(self, func: Callable[[Any], T], name: str = "") -> None:
        self.func, self.name = func, name or getattr(func, "__name__", "validator")

    def __call__(self, value: Any) -> T:
        return self.func(value)

    def __rshift__(self, other: Validator[U]) -> Validator[U]:
        return Validator(lambda v: other(self(v)), f"{self.name} >> {other.name}")

    def optional(self) -> Validator[T | None]:
        return Validator(lambda v: None if v is None or (isinstance(v, str) and not v.strip()) else self(v),
                         f"optional({self.name})")

    def default(self, fallback: T) -> Validator[T]:
        return Validator(lambda v: fallback if v is None or v == "" else self(v), f"default({self.name})")

    def check(self, predicate: Callable[[T], bool], message: str) -> Validator[T]:
        def run(v: Any) -> T:
            result = self(v)
            if not predicate(result):
                raise ValidationError(message, value=result)
            return result

        return Validator(run, self.name)


# --- cleaning helpers ---------------------------------------------------------
def squash(value: str) -> str:
    return " ".join(value.split())


def parse_measurement(value: str | float, unit: str) -> Decimal:
    """``"72,5 kg"`` → ``Decimal("72.5")``; rejects a different unit."""
    text = str(value).strip().lower().replace(",", ".")
    match = re.fullmatch(r"(-?\d+(?:\.\d+)?)\s*([a-z]*)", text)
    if not match or match[2] not in {"", unit}:
        raise ValidationError(f"expected a number in {unit}", value=value)
    try:
        return Decimal(match[1])
    except InvalidOperation:  # pragma: no cover - regex already guarantees digits
        raise ValidationError("not a number", value=value) from None


# --- validator factories --------------------------------------------------------
def text(*, min_len: int = 1, max_len: int = 200, pattern: str | None = None) -> Validator[str]:
    compiled = re.compile(pattern) if pattern else None

    def run(value: Any) -> str:
        if not isinstance(value, str):
            raise ValidationError("must be text", value=value)
        cleaned = squash(value)
        if not min_len <= len(cleaned) <= max_len:
            raise ValidationError(f"length must be {min_len}–{max_len}", value=value)
        if compiled and not compiled.fullmatch(cleaned):
            raise ValidationError("has an invalid format", value=value)
        return cleaned

    return Validator(run, "text")


def number(unit: str = "", *, low: Decimal | int | None = None, high: Decimal | int | None = None) -> Validator[Decimal]:
    def run(value: Any) -> Decimal:
        if isinstance(value, bool):
            raise ValidationError("must be a number", value=value)
        result = parse_measurement(value, unit) if isinstance(value, str) else Decimal(str(value))
        if (low is not None and result < low) or (high is not None and result > high):
            raise ValidationError(f"must be between {low} and {high}{' ' + unit if unit else ''}", value=value)
        return result

    return Validator(run, f"number({unit})")


def day(*formats: str, not_future: bool = True, today: Callable[[], date] = date.today) -> Validator[date]:
    formats = formats or ("%Y-%m-%d", "%d.%m.%Y", "%Y/%m/%d")

    def run(value: Any) -> date:
        if isinstance(value, date):
            result = value
        else:
            for fmt in formats:
                try:
                    result = datetime.strptime(str(value).strip(), fmt).date()
                    break
                except ValueError:
                    continue
            else:
                raise ValidationError(f"not a date ({' or '.join(formats)})", value=value)
        if not_future and result > today():
            raise ValidationError("cannot be in the future", value=value)
        return result

    return Validator(run, "day")


def one_of(*choices: str, aliases: Mapping[str, str] | None = None) -> Validator[str]:
    lookup = {c.lower(): c for c in choices} | {k.lower(): v for k, v in (aliases or {}).items()}

    def run(value: Any) -> str:
        key = squash(str(value)).lower()
        if key not in lookup:
            raise ValidationError(f"must be one of {', '.join(choices)}", value=value)
        return lookup[key]

    return Validator(run, "one_of")


def list_of[V](item: Validator[V], *, min_items: int = 0) -> Validator[list[V]]:
    def run(value: Any) -> list[V]:
        if not isinstance(value, list | tuple):
            raise ValidationError("must be a list", value=value)
        if len(value) < min_items:
            raise ValidationError(f"needs at least {min_items} item(s)", value=value)
        results, errors = [], []
        for index, element in enumerate(value):
            try:
                results.append(item(element))
            except ValidationError as exc:
                errors.extend(_flatten(exc.at(f"[{index}]")))
        if errors:
            raise SchemaError(errors)
        return results

    return Validator(run, f"list_of({item.name})")


def _flatten(exc: ValidationError) -> list[ValidationError]:
    return exc.errors if isinstance(exc, SchemaError) else [exc]


def schema(fields: Mapping[str, Validator[Any]], *, allow_extra: bool = False) -> Validator[dict[str, Any]]:
    """Validate every field (never stop at the first error) and report them together."""

    def run(value: Any) -> dict[str, Any]:
        if not isinstance(value, Mapping):
            raise ValidationError("must be an object", value=value)
        cleaned: dict[str, Any] = {}
        errors: list[ValidationError] = []
        for name, validator in fields.items():
            try:
                cleaned[name] = validator(value.get(name))
            except ValidationError as exc:
                errors.extend(_flatten(exc.at(name)))
        if not allow_extra:
            errors += [ValidationError("unexpected field", key) for key in value if key not in fields]
        if errors:
            raise SchemaError(errors)
        return cleaned

    return Validator(run, "schema")


@dataclass
class BatchReport:
    clean: list[dict[str, Any]]
    rejected: list[tuple[int, list[str]]]

    @property
    def pass_rate(self) -> float:
        total = len(self.clean) + len(self.rejected)
        return round(len(self.clean) / total, 3) if total else 1.0


def validate_batch(rows: Iterable[Mapping[str, Any]], validator: Validator[dict[str, Any]]) -> BatchReport:
    report = BatchReport([], [])
    for number, row in enumerate(rows, start=1):
        try:
            report.clean.append(validator(row))
        except ValidationError as exc:
            report.rejected.append((number, [str(e) for e in _flatten(exc)]))
    return report


def patient_schema(today: Callable[[], date] = date.today) -> Validator[dict[str, Any]]:
    visit = schema({"date": day(today=today), "systolic": number("mmhg", low=60, high=250)})
    return schema({
        "patient_id": text(pattern=r"PT-\d{5}") >> Validator(str.upper, "upper"),
        "name": text(max_len=80),
        "sex": one_of("female", "male", "other", aliases={"f": "female", "m": "male"}),
        "born": day(today=today).check(lambda d: d.year >= 1900, "must be after 1900"),
        "weight": number("kg", low=2, high=400),
        "email": text(pattern=r"[^@\s]+@[^@\s]+\.[a-z]{2,}").optional(),
        "consent": one_of("yes", "no").default("no").check(lambda c: c == "yes", "consent is required"),
        "visits": list_of(visit, min_items=1),
    })


SAMPLE_ROWS: list[dict[str, Any]] = [
    {"patient_id": "PT-00417", "name": "  Maria   Silva ", "sex": " F ", "born": "07.03.1980", "weight": "72,5 kg",
     "email": "", "consent": "YES", "visits": [{"date": "2026-09-01", "systolic": "128 mmHg"}]},
    {"patient_id": "pt-1", "name": "", "sex": "unknown", "born": "2099-01-01", "weight": "72 lb", "consent": None,
     "visits": [{"date": "2026-09-01", "systolic": 120}, {"date": "yesterday", "systolic": "300"}], "notes": "x"},
]


def main() -> None:
    print("Day 94 – Patient intake validation\n")
    report = validate_batch(SAMPLE_ROWS, patient_schema(lambda: date(2026, 10, 1)))
    print("clean:", report.clean[0])
    for row, problems in report.rejected:
        print(f"row {row} rejected:")
        for problem in problems:
            print("   -", problem)
    print("pass rate:", report.pass_rate)


if __name__ == "__main__":
    main()
