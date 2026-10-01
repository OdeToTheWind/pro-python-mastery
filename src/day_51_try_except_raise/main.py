"""Day 51 – Try / Except / Raise.

Scenario: a *concert ticket booking service* with its own exception hierarchy,
so callers can catch errors as broadly or as precisely as they need.

Deliverables (syllabus):
* Raising custom exceptions (with data attributes and helpful messages)
* Exception hierarchy design (a base class, categories, specific errors)
* Catching at different levels of the hierarchy; re-raising and translating
"""

from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal

DELIVERABLES: dict[str, str] = {
    "custom exception base class": "BookingError",
    "exception hierarchy design": "exception_tree",
    "exceptions carrying data": "SeatUnavailableError",
    "raise": "BookingService.book",
    "catching by level of the hierarchy": "handle_booking",
    "translating low-level errors (raise from)": "BookingService.charge",
}


class BookingError(Exception):
    """Base class – ``except BookingError`` catches every booking problem."""

    code = "BOOKING"


class ValidationError(BookingError):
    code = "INVALID"


class InvalidSeatError(ValidationError):
    code = "INVALID_SEAT"


class TooManyTicketsError(ValidationError):
    code = "TOO_MANY"

    def __init__(self, requested: int, limit: int) -> None:
        super().__init__(f"requested {requested} tickets, limit is {limit}")
        self.requested, self.limit = requested, limit


class AvailabilityError(BookingError):
    code = "UNAVAILABLE"


class SeatUnavailableError(AvailabilityError):
    code = "SEAT_TAKEN"

    def __init__(self, seats: list[str]) -> None:
        super().__init__(f"already booked: {', '.join(seats)}")
        self.seats = seats


class SoldOutError(AvailabilityError):
    code = "SOLD_OUT"


class PaymentError(BookingError):
    code = "PAYMENT"


class CardDeclinedError(PaymentError):
    code = "DECLINED"


@dataclass
class BookingService:
    rows: str = "ABC"
    seats_per_row: int = 4
    price: Decimal = Decimal("45")
    max_per_order: int = 4
    taken: set[str] = field(default_factory=set)

    def all_seats(self) -> set[str]:
        return {f"{r}{n}" for r in self.rows for n in range(1, self.seats_per_row + 1)}

    def charge(self, card: str, amount: Decimal) -> str:
        """Translate a low-level ``ValueError`` into the domain's ``CardDeclinedError``."""
        try:
            if not card.isdigit() or len(card) != 16:
                raise ValueError("card number must be 16 digits")
            if card.endswith("0000"):
                raise ValueError("issuer declined")
        except ValueError as exc:
            raise CardDeclinedError(str(exc)) from exc
        return f"PAY-{card[-4:]}-{amount}"

    def book(self, seats: list[str], card: str) -> str:
        if not seats:
            raise ValidationError("choose at least one seat")
        if len(seats) > self.max_per_order:
            raise TooManyTicketsError(len(seats), self.max_per_order)
        unknown = sorted(set(seats) - self.all_seats())
        if unknown:
            raise InvalidSeatError(f"no such seat(s): {', '.join(unknown)}")
        if self.taken >= self.all_seats():
            raise SoldOutError("the show is sold out")
        clashes = sorted(set(seats) & self.taken)
        if clashes:
            raise SeatUnavailableError(clashes)
        reference = self.charge(card, self.price * len(seats))
        self.taken.update(seats)
        return reference


def exception_tree(root: type[BaseException] = BookingError, depth: int = 0) -> list[str]:
    """Render the hierarchy by walking ``__subclasses__()``."""
    lines = [f"{'  ' * depth}{root.__name__} [{getattr(root, 'code', '')}]"]
    for sub in root.__subclasses__():
        lines.extend(exception_tree(sub, depth + 1))
    return lines


def handle_booking(service: BookingService, seats: list[str], card: str) -> str:
    """Catch the most specific errors first, then categories, then the base."""
    try:
        return f"confirmed {service.book(seats, card)}"
    except SeatUnavailableError as exc:
        free = sorted(service.all_seats() - service.taken)[:3]
        return f"{exc.code}: {exc} – try {', '.join(free)}"
    except ValidationError as exc:
        return f"{exc.code}: please fix your request ({exc})"
    except PaymentError as exc:
        return f"{exc.code}: payment failed ({exc}); cause={type(exc.__cause__).__name__}"
    except BookingError as exc:
        return f"{exc.code}: {exc}"


def main() -> None:
    print("Day 51 – Ticket booking exceptions\n")
    print("\n".join(exception_tree()))
    service = BookingService()
    card = "4111111111111111"
    for seats, used_card in [(["A1", "A2"], card), (["A2"], card), (["Z9"], card),
                             (["B1"] * 5, card), (["C1"], "4111111111110000")]:
        print(f"\n{seats!s:<36} → {handle_booking(service, seats, used_card)}")


if __name__ == "__main__":
    main()
