"""Tests for Day 51 – Custom Exceptions and Hierarchies."""

from decimal import Decimal

import pytest

from src.day_51_try_except_raise.main import (
    AvailabilityError,
    BookingError,
    BookingService,
    CardDeclinedError,
    InvalidSeatError,
    PaymentError,
    SeatUnavailableError,
    SoldOutError,
    TooManyTicketsError,
    ValidationError,
    exception_tree,
    handle_booking,
    main,
)

CARD = "4111111111111111"


@pytest.fixture
def service():
    return BookingService()


def test_hierarchy():
    assert issubclass(InvalidSeatError, ValidationError)
    assert issubclass(SeatUnavailableError, AvailabilityError)
    assert issubclass(CardDeclinedError, PaymentError)
    assert all(issubclass(e, BookingError) for e in (ValidationError, AvailabilityError, PaymentError))
    assert not issubclass(BookingError, ValueError)


def test_successful_booking(service):
    assert service.book(["A1", "A2"], CARD) == "PAY-1111-90"
    assert service.taken == {"A1", "A2"}


@pytest.mark.parametrize(
    ("seats", "error"),
    [([], ValidationError), (["A1"] * 5, TooManyTicketsError), (["Z1"], InvalidSeatError)],
)
def test_validation_errors(service, seats, error):
    with pytest.raises(error):
        service.book(seats, CARD)


def test_exceptions_carry_data(service):
    service.book(["A1"], CARD)
    with pytest.raises(SeatUnavailableError) as info:
        service.book(["A1", "A2"], CARD)
    assert info.value.seats == ["A1"] and info.value.code == "SEAT_TAKEN"
    with pytest.raises(TooManyTicketsError) as info2:
        service.book(["A1"] * 9, CARD)
    assert (info2.value.requested, info2.value.limit) == (9, 4)


def test_sold_out(service):
    service.taken = service.all_seats()
    with pytest.raises(SoldOutError):
        service.book(["A1"], CARD)


def test_payment_errors_are_translated_and_chained(service):
    with pytest.raises(CardDeclinedError) as info:
        service.book(["B1"], "123")
    assert isinstance(info.value.__cause__, ValueError)
    assert "B1" not in service.taken  # nothing booked when payment fails


def test_catch_by_category(service):
    with pytest.raises(BookingError):
        service.book(["Q1"], CARD)


def test_handle_booking_messages(service):
    assert handle_booking(service, ["A1"], CARD).startswith("confirmed")
    assert handle_booking(service, ["A1"], CARD) == "SEAT_TAKEN: already booked: A1 – try A2, A3, A4"
    assert handle_booking(service, ["X"], CARD).startswith("INVALID_SEAT: please fix")
    assert handle_booking(service, ["B2"], "4111111111110000") == (
        "DECLINED: payment failed (issuer declined); cause=ValueError")
    service.taken = service.all_seats()
    assert handle_booking(service, ["C1"], CARD) == "SOLD_OUT: the show is sold out"


def test_exception_tree():
    tree = exception_tree()
    assert tree[0] == "BookingError [BOOKING]"
    assert "    InvalidSeatError [INVALID_SEAT]" in tree
    assert len(tree) == 9  # base + 3 categories + 5 specific errors


def test_price_is_decimal(service):
    assert service.price == Decimal("45")


def test_main(capsys):
    main()
    assert "TOO_MANY" in capsys.readouterr().out
