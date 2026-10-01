"""Tests for Day 69 – Descriptors."""

import datetime as dt

import pytest

from src.day_69_descriptors.main import (
    Booking,
    Field,
    MyProperty,
    PositiveInt,
    bound_method_demo,
    cached,
    main,
    precedence_demo,
)

DAY = dt.date(2026, 11, 3)


def make(**overrides):
    data = {"guest": "Ada", "check_in": DAY, "nights": 3, "guests": 2, **overrides}
    return Booking(**data)


def test_fields_store_validated_values():
    booking = make(guest="  Ada  ")
    assert booking.guest == "Ada"
    assert booking.__dict__["_guest"] == "Ada"


@pytest.mark.parametrize(
    "overrides",
    [{"nights": 0}, {"nights": 31}, {"guests": 5}, {"guests": True}, {"guest": ""},
     {"check_in": dt.date(2025, 12, 31)}, {"check_in": "2026-11-03"}],
)
def test_invalid_values_rejected(overrides):
    with pytest.raises(ValueError):
        make(**overrides)


def test_set_name_and_class_access():
    assert isinstance(Booking.nights, PositiveInt)
    assert (Booking.nights.public_name, Booking.nights.private_name) == ("nights", "_nights")


def test_unset_and_delete():
    class Room:
        number = Field()

    with pytest.raises(AttributeError, match="has not been set"):
        _ = Room().number
    booking = make()
    with pytest.raises(AttributeError, match="cannot be deleted"):
        del booking.nights


def test_each_instance_has_its_own_values():
    a, b = make(nights=2), make(nights=5)
    assert (a.nights, b.nights) == (2, 5)


def test_my_property_getter_and_setter():
    booking = make()
    assert booking.check_out == dt.date(2026, 11, 6)
    booking.check_out = dt.date(2026, 11, 10)
    assert booking.nights == 7
    assert isinstance(Booking.__dict__["check_out"], MyProperty)
    assert Booking.check_out.__doc__ == "Derived from check-in and nights."


def test_my_property_read_only():
    class Thing:
        @MyProperty
        def x(self):
            return 1

    with pytest.raises(AttributeError):
        Thing().x = 2


def test_cached_non_data_descriptor_computes_once():
    descriptor = Booking.__dict__["quote"]
    assert isinstance(descriptor, cached)
    before = descriptor.calls
    booking = make()
    assert booking.quote == booking.quote == 120 * 3 + 25 * 3
    assert descriptor.calls == before + 1
    assert "quote" in booking.__dict__


def test_lookup_precedence():
    assert precedence_demo(make()) == {"nights": 3, "quote": "manual"}


def test_functions_are_descriptors():
    assert bound_method_demo(make()) == (True, True)


def test_main(capsys):
    main()
    out = capsys.readouterr().out
    assert "nights = 5" in out and out.count("rejected:") == 3
