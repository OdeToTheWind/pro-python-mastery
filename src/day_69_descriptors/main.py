"""Day 69 – Descriptors.

Scenario: a *hotel-booking form model* whose fields validate themselves – the
same machinery behind Django/SQLAlchemy model fields, ``@property``,
``@classmethod`` and bound methods.

Deliverables (syllabus):
* Data descriptors (``__get__`` + ``__set__``/``__delete__``)
* Non-data descriptors (``__get__`` only)
* How ``@property`` works under the hood (a pure-Python re-implementation)
"""

from __future__ import annotations

import datetime as dt
from collections.abc import Callable
from typing import Any, overload

DELIVERABLES: dict[str, str] = {
    "data descriptor with __set_name__": "Field",
    "validated descriptor subclasses": "PositiveInt",
    "non-data descriptor (cached value)": "cached",
    "lookup precedence: data > instance dict > non-data": "precedence_demo",
    "@property re-implemented": "MyProperty",
    "functions are non-data descriptors (bound methods)": "bound_method_demo",
}

class Field[T]:
    """A **data** descriptor: defines ``__set__`` so it always wins over ``obj.__dict__``."""

    def __set_name__(self, owner: type, name: str) -> None:
        self.public_name = name
        self.private_name = f"_{name}"

    @overload
    def __get__(self, obj: None, objtype: type | None = None) -> Field[T]: ...
    @overload
    def __get__(self, obj: object, objtype: type | None = None) -> T: ...
    def __get__(self, obj: object | None, objtype: type | None = None) -> Any:
        if obj is None:
            return self  # accessed on the class: return the descriptor itself
        try:
            return getattr(obj, self.private_name)
        except AttributeError:
            raise AttributeError(f"{self.public_name!r} has not been set") from None

    def __set__(self, obj: object, value: T) -> None:
        setattr(obj, self.private_name, self.validate(value))

    def __delete__(self, obj: object) -> None:
        raise AttributeError(f"{self.public_name!r} cannot be deleted")

    def validate(self, value: Any) -> T:
        return value  # type: ignore[no-any-return]


class NonEmptyStr(Field[str]):
    def validate(self, value: Any) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{self.public_name} must be a non-empty string")
        return value.strip()


class PositiveInt(Field[int]):
    def __init__(self, maximum: int | None = None) -> None:
        self.maximum = maximum

    def validate(self, value: Any) -> int:
        if not isinstance(value, int) or isinstance(value, bool) or value < 1:
            raise ValueError(f"{self.public_name} must be a positive integer")
        if self.maximum is not None and value > self.maximum:
            raise ValueError(f"{self.public_name} must be ≤ {self.maximum}")
        return value


class FutureDate(Field[dt.date]):
    def validate(self, value: Any) -> dt.date:
        if not isinstance(value, dt.date) or value <= dt.date(2026, 1, 1):
            raise ValueError(f"{self.public_name} must be a date after 2026-01-01")
        return value


class cached:  # noqa: N801 – lower-case like functools.cached_property
    """A **non-data** descriptor (only ``__get__``): computes once, then stores the
    value in the instance ``__dict__``, which shadows the descriptor afterwards."""

    def __init__(self, func: Callable[[Any], Any]) -> None:
        self.func = func
        self.name = func.__name__
        self.calls = 0

    def __get__(self, obj: object | None, objtype: type | None = None) -> Any:
        if obj is None:
            return self
        self.calls += 1
        value = self.func(obj)
        obj.__dict__[self.name] = value
        return value


class MyProperty:
    """What ``property`` does, in ~20 lines of Python."""

    def __init__(self, fget: Callable[[Any], Any], fset: Callable[[Any, Any], None] | None = None) -> None:
        self.fget, self.fset = fget, fset
        self.__doc__ = fget.__doc__

    def __get__(self, obj: object | None, objtype: type | None = None) -> Any:
        return self if obj is None else self.fget(obj)

    def __set__(self, obj: object, value: Any) -> None:
        if self.fset is None:
            raise AttributeError("can't set attribute")
        self.fset(obj, value)

    def setter(self, fset: Callable[[Any, Any], None]) -> MyProperty:
        return type(self)(self.fget, fset)  # like property.setter: returns a new descriptor


class Booking:
    guest = NonEmptyStr()
    nights = PositiveInt(maximum=30)
    guests = PositiveInt(maximum=4)
    check_in = FutureDate()
    RATE = 120

    def __init__(self, guest: str, check_in: dt.date, nights: int, guests: int = 1) -> None:
        self.guest, self.check_in, self.nights, self.guests = guest, check_in, nights, guests

    @MyProperty
    def check_out(self) -> dt.date:
        """Derived from check-in and nights."""
        return self.check_in + dt.timedelta(days=self.nights)

    @check_out.setter  # type: ignore[no-redef]  # mypy only special-cases the built-in property
    def check_out(self, value: dt.date) -> None:
        self.nights = (value - self.check_in).days

    @cached
    def quote(self) -> int:
        return self.RATE * self.nights + 25 * (self.guests - 1) * self.nights


def precedence_demo(booking: Booking) -> dict[str, object]:
    """Data descriptors beat the instance dict; the instance dict beats non-data descriptors."""
    booking.__dict__["nights"] = 999  # ignored: `nights` is a data descriptor
    booking.__dict__["quote"] = "manual"  # wins: `quote` is a non-data descriptor
    return {"nights": booking.nights, "quote": booking.quote}


def bound_method_demo(booking: Booking) -> tuple[bool, bool]:
    """``Booking.__init__`` is a plain function; ``booking.__init__`` is a bound method
    produced by the function's own ``__get__``."""
    func = Booking.__dict__["__init__"]
    bound = func.__get__(booking, Booking)
    return bound.__self__ is booking, bound.__func__ is func


def main() -> None:
    print("Day 69 – Self-validating booking model\n")
    booking = Booking("  Ada Lovelace ", dt.date(2026, 11, 3), nights=3, guests=2)
    print(booking.guest, booking.check_in, "→", booking.check_out, "quote €", booking.quote)
    booking.check_out = dt.date(2026, 11, 8)  # type: ignore[method-assign]
    print("after moving check-out: nights =", booking.nights)
    for bad in ({"nights": 0}, {"guests": 9}, {"guest": "  "}):
        try:
            fields: dict[str, Any] = {"guest": "x", "check_in": dt.date(2026, 5, 1), "nights": 1, **bad}
            Booking(**fields)
        except ValueError as exc:
            print("rejected:", exc)
    print("descriptor on class:", Booking.nights, "| precedence:", precedence_demo(booking))
    print("bound method:", bound_method_demo(booking))


if __name__ == "__main__":
    main()
