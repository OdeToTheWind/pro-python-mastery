"""Day 03 – Input & Print Functions.

Scenario: a *workshop registration desk* that asks attendees questions in the
console, validates every answer and prints a receipt.

Deliverables (syllabus):
* User input validation
* Type conversion of typed text
* Interactive console applications (with clean exit on EOF / Ctrl-D)
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

DELIVERABLES: dict[str, str] = {
    "input validation": "ask",
    "type conversion": "to_int_in_range",
    "interactive console application": "register",
    "formatted print output": "format_receipt",
}

Asker = Callable[[str], str]
Printer = Callable[[str], None]

TICKET_PRICES = {"student": 15.0, "standard": 40.0, "vip": 95.0}


class RegistrationCancelled(Exception):
    """Raised when the attendee closes the input stream or types 'cancel'."""


@dataclass(frozen=True, slots=True)
class Registration:
    name: str
    age: int
    ticket: str
    guests: int

    @property
    def total(self) -> float:
        return TICKET_PRICES[self.ticket] * (1 + self.guests)


def to_int_in_range(text: str, low: int, high: int) -> int:
    """Convert *text* to ``int`` and check ``low <= value <= high``."""
    value = int(text)  # raises ValueError for "abc" or "4.5"
    if not low <= value <= high:
        raise ValueError(f"must be between {low} and {high}")
    return value


def non_empty(text: str) -> str:
    if not text:
        raise ValueError("cannot be empty")
    return " ".join(text.split())


def one_of(*choices: str) -> Callable[[str], str]:
    def check(text: str) -> str:
        value = text.lower()
        if value not in choices:
            raise ValueError(f"choose one of: {', '.join(choices)}")
        return value

    return check


def ask[T](
    prompt: str,
    convert: Callable[[str], T],
    *,
    ask_fn: Asker = input,
    print_fn: Printer = print,
    max_attempts: int = 3,
) -> T:
    """Prompt until *convert* accepts the answer.

    * ``ValueError`` from *convert* → explain and retry (up to *max_attempts*)
    * ``EOFError`` (Ctrl-D / closed pipe) or ``cancel`` → ``RegistrationCancelled``
    """
    for attempt in range(1, max_attempts + 1):
        try:
            raw = ask_fn(prompt).strip()
        except EOFError as exc:
            raise RegistrationCancelled("input stream closed") from exc
        if raw.lower() == "cancel":
            raise RegistrationCancelled("cancelled by user")
        try:
            return convert(raw)
        except ValueError as exc:
            remaining = max_attempts - attempt
            print_fn(f"  ✗ {exc}. {remaining} attempt(s) left.")
    raise RegistrationCancelled("too many invalid answers")


def register(ask_fn: Asker = input, print_fn: Printer = print) -> Registration:
    """Run the interactive registration conversation."""
    name = ask("Full name: ", non_empty, ask_fn=ask_fn, print_fn=print_fn)
    age = ask(
        "Age (12-120): ", lambda t: to_int_in_range(t, 12, 120), ask_fn=ask_fn, print_fn=print_fn
    )
    default_ticket = "student" if age < 25 else "standard"
    ticket = ask(
        f"Ticket [student/standard/vip] (Enter = {default_ticket}): ",
        lambda t: one_of(*TICKET_PRICES)(t or default_ticket),
        ask_fn=ask_fn,
        print_fn=print_fn,
    )
    guests = ask(
        "Number of guests (0-3): ",
        lambda t: to_int_in_range(t or "0", 0, 3),
        ask_fn=ask_fn,
        print_fn=print_fn,
    )
    return Registration(name, age, ticket, guests)


def format_receipt(reg: Registration) -> str:
    """Format a receipt with aligned labels, padding and currency precision."""
    rows = [
        ("Attendee", reg.name),
        ("Age", f"{reg.age:>3}"),
        ("Ticket", reg.ticket.upper()),
        ("Guests", f"{reg.guests:>3}"),
        ("Total", f"€{reg.total:>8.2f}"),
    ]
    width = 36
    body = "\n".join(f"{label:<10}: {value}" for label, value in rows)
    return f"{' RECEIPT ':=^{width}}\n{body}\n{'=' * width}"


def main(ask_fn: Asker = input, print_fn: Printer = print) -> None:
    print_fn("Day 03 – Workshop registration (type 'cancel' to stop)")
    try:
        reg = register(ask_fn, print_fn)
    except RegistrationCancelled as exc:
        print_fn(f"Registration cancelled: {exc}")
        return
    print_fn(format_receipt(reg))


if __name__ == "__main__":
    main()
