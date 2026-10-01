"""Tests for Day 94 – Data Validation & Cleaning Library."""

from datetime import date
from decimal import Decimal

import pytest

from src.day_94_data_validation_library.main import (
    SAMPLE_ROWS,
    SchemaError,
    ValidationError,
    Validator,
    day,
    list_of,
    main,
    number,
    one_of,
    parse_measurement,
    patient_schema,
    schema,
    text,
    validate_batch,
)

TODAY = date(2026, 10, 1)


def errors_of(validator, value):
    with pytest.raises(ValidationError) as info:
        validator(value)
    exc = info.value
    return [str(e) for e in exc.errors] if isinstance(exc, SchemaError) else [str(exc)]


@pytest.mark.parametrize(("raw", "unit", "value"), [("72,5 kg", "kg", "72.5"), ("80", "kg", "80"),
                                                    (" 120 MMHG ", "mmhg", "120"), (3.5, "kg", "3.5")])
def test_parse_measurement(raw, unit, value):
    assert parse_measurement(raw, unit) == Decimal(value)


@pytest.mark.parametrize("raw", ["72 lb", "heavy", "7.2.1"])
def test_parse_measurement_rejects(raw):
    with pytest.raises(ValidationError, match="in kg"):
        parse_measurement(raw, "kg")


def test_text_validator_cleans_and_checks():
    v = text(min_len=2, max_len=5, pattern=r"[a-z ]+")
    assert v("  ab   c ") == "ab c"
    assert errors_of(v, 5) == ["must be text"] and errors_of(v, "a") == ["length must be 2–5"]
    assert errors_of(v, "AB") == ["has an invalid format"]


def test_number_bounds_and_bool_guard():
    v = number("kg", low=2, high=10)
    assert v(5) == Decimal("5") and v("2,0kg") == Decimal("2.0")
    assert errors_of(v, "11") == ["must be between 2 and 10 kg"] and errors_of(v, True) == ["must be a number"]


def test_day_formats_and_future():
    v = day(today=lambda: TODAY)
    assert v("2026/09/30") == v("30.09.2026") == v(date(2026, 9, 30)) == date(2026, 9, 30)
    assert errors_of(v, "2026-10-02") == ["cannot be in the future"]
    assert "not a date" in errors_of(v, "soon")[0]
    assert day("%d %b %Y", not_future=False)("01 Jan 2030") == date(2030, 1, 1)


def test_composition_optional_default_check():
    upper = Validator(str.upper, "upper")
    code = text() >> upper
    assert code(" ab ") == "AB" and code.name == "text >> upper"
    assert text().optional()("   ") is None and text().optional()(None) is None
    assert one_of("yes", "no").default("no")("") == "no"
    positive = number().check(lambda n: n > 0, "must be positive")
    assert errors_of(positive, "-1") == ["must be positive"]


def test_one_of_aliases():
    v = one_of("female", "male", aliases={"F": "female"})
    assert v(" f ") == "female" and v("MALE") == "male"
    assert errors_of(v, "x") == ["must be one of female, male"]


def test_nested_errors_have_paths():
    v = schema({"name": text(), "visits": list_of(schema({"bp": number(low=60)}), min_items=1)})
    assert errors_of(v, {"name": "A", "visits": [{"bp": 70}, {"bp": 20}, {"bp": "x"}], "extra": 1}) == [
        "visits[1].bp: must be between 60 and None", "visits[2].bp: expected a number in ",
        "extra: unexpected field"]
    assert errors_of(v, {"name": "", "visits": []}) == ["name: length must be 1–200",
                                                       "visits: needs at least 1 item(s)"]
    assert errors_of(v, "nope") == ["must be an object"]
    assert errors_of(list_of(text()), "nope") == ["must be a list"]
    assert schema({"a": text()}, allow_extra=True)({"a": "x", "b": 1}) == {"a": "x"}


def test_schema_error_message_counts_problems():
    with pytest.raises(SchemaError, match=r"^2 problem\(s\): a: must be text; b: must be text$"):
        schema({"a": text(), "b": text()})({})


def test_patient_batch_report():
    report = validate_batch(SAMPLE_ROWS, patient_schema(lambda: TODAY))
    clean = report.clean[0]
    assert clean["name"] == "Maria Silva" and clean["sex"] == "female" and clean["weight"] == Decimal("72.5")
    assert clean["email"] is None and clean["visits"][0]["systolic"] == Decimal("128")
    row, problems = report.rejected[0]
    assert row == 2 and problems == [
        "patient_id: has an invalid format", "name: length must be 1–80", "sex: must be one of female, male, other",
        "born: cannot be in the future", "weight: expected a number in kg", "consent: consent is required",
        "visits[1].date: not a date (%Y-%m-%d or %d.%m.%Y or %Y/%m/%d)",
        "visits[1].systolic: must be between 60 and 250 mmhg", "notes: unexpected field"]
    assert report.pass_rate == 0.5 and validate_batch([], patient_schema()).pass_rate == 1.0


def test_main(capsys):
    main()
    out = capsys.readouterr().out
    assert "row 2 rejected:" in out and "pass rate: 0.5" in out
