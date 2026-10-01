"""Day 81 – Advanced Regular Expressions.

Scenario: a *customer-support ticket parser* that pulls order numbers,
amounts, dates and contact details out of free-text emails, redacts personal
data before it reaches the logs, and normalises messy formatting.

Deliverables (syllabus):
* Complex patterns (verbose mode with comments, alternation, quantifiers, flags)
* Groups (named, non-capturing, backreferences, ``groupdict``)
* Lookarounds (lookahead, negative lookahead, lookbehind)
* The ``re`` module API (compile, search, fullmatch, finditer, sub with a
  function, split) – and avoiding catastrophic backtracking
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from decimal import Decimal

DELIVERABLES: dict[str, str] = {
    "verbose pattern with comments": "ORDER_RE",
    "named groups + groupdict": "parse_amounts",
    "non-capturing groups and alternation": "DATE_RE",
    "backreferences": "find_repeated_words",
    "lookahead / negative lookahead": "is_strong_reference",
    "lookbehind": "parse_amounts",
    "sub with a replacement function": "redact",
    "split on a pattern": "split_sentences",
    "fullmatch for validation": "valid_order_number",
    "safe vs catastrophic patterns": "SAFE_EMAIL_RE",
}

ORDER_RE = re.compile(
    r"""
    \b
    (?P<prefix>ORD|INV)        # order or invoice
    [-\s]?                     # optional separator
    (?P<year>20\d{2})          # four-digit year 2000-2099
    [-\s]?
    (?P<number>\d{5})          # five-digit sequence
    \b
    """,
    re.VERBOSE | re.IGNORECASE,
)

AMOUNT_RE = re.compile(r"(?<=[€$£])\s?(?P<value>\d{1,3}(?:[,.]\d{3})*(?:[.,]\d{2})?)|(?P<value2>\d+(?:\.\d{2})?)\s?(?:EUR|USD)\b")

DATE_RE = re.compile(
    r"\b(?:(?P<iso>\d{4}-\d{2}-\d{2})|(?P<day>\d{1,2})[./](?P<month>\d{1,2})[./](?P<year>\d{4}))\b"
)

# Linear-time email pattern: no nested quantifiers like (\w+)+ that explode on bad input.
SAFE_EMAIL_RE = re.compile(r"\b[\w.+-]{1,64}@[\w-]{1,63}(?:\.[\w-]{1,63})+\b")
CATASTROPHIC_EXAMPLE = r"^(\w+\s?)*$"  # documented only – never run on untrusted input
PHONE_RE = re.compile(r"(?<!\d)(?:\+\d{1,3}[\s-]?)?(?:\(?\d{2,4}\)?[\s-]?)?\d{3,4}[\s-]?\d{3,4}(?!\d)")
REPEAT_RE = re.compile(r"\b(\w+)\s+\1\b", re.IGNORECASE)
REFERENCE_RE = re.compile(r"^(?=.*\d)(?=.*[A-Z])(?!(?i:.*(?:password|1234)))[A-Za-z\d-]{8,}$")


@dataclass(frozen=True, slots=True)
class OrderRef:
    kind: str
    year: int
    number: str

    def __str__(self) -> str:
        return f"{self.kind}-{self.year}-{self.number}"


def find_orders(text: str) -> list[OrderRef]:
    """``finditer`` yields Match objects; normalise every variant to one format."""
    return [OrderRef(m["prefix"].upper(), int(m["year"]), m["number"]) for m in ORDER_RE.finditer(text)]


def valid_order_number(candidate: str) -> bool:
    """``fullmatch`` – the *whole* string must match, not just a part of it."""
    return ORDER_RE.fullmatch(candidate.strip()) is not None


def parse_amounts(text: str) -> list[Decimal]:
    """Lookbehind ``(?<=€)`` matches the number only when a currency symbol precedes it."""
    amounts = []
    for match in AMOUNT_RE.finditer(text):
        groups = match.groupdict()
        raw = groups["value"] or groups["value2"]
        if re.search(r",\d{2}$", raw):  # European decimal comma: 1.234,56
            raw = raw.replace(".", "").replace(",", ".")
        else:
            raw = raw.replace(",", "")
        amounts.append(Decimal(raw))
    return amounts


def parse_dates(text: str) -> list[str]:
    """Alternation inside a non-capturing group accepts ISO and day/month/year."""
    dates = []
    for m in DATE_RE.finditer(text):
        if m["iso"]:
            dates.append(m["iso"])
        else:
            dates.append(f"{int(m['year']):04d}-{int(m['month']):02d}-{int(m['day']):02d}")
    return dates


def find_repeated_words(text: str) -> list[str]:
    """Backreference ``\\1`` matches the *same* text the first group captured."""
    return [m.group(1).lower() for m in REPEAT_RE.finditer(text)]


def is_strong_reference(code: str) -> bool:
    """Lookaheads test several conditions at one position without consuming text."""
    return REFERENCE_RE.match(code) is not None


def redact(text: str) -> str:
    """``sub`` with a function keeps the domain / last digits so agents can still triage."""

    def mask_email(m: re.Match[str]) -> str:
        user, domain = m.group(0).split("@", 1)
        return f"{user[0]}***@{domain}"

    def mask_phone(m: re.Match[str]) -> str:
        digits = re.sub(r"\D", "", m.group(0))
        return f"[phone …{digits[-2:]}]"

    return PHONE_RE.sub(mask_phone, SAFE_EMAIL_RE.sub(mask_email, text))


def split_sentences(text: str) -> list[str]:
    """Split after . ! ? followed by whitespace and a capital letter (lookahead)."""
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+(?=[A-Z])", text) if s.strip()]


def normalise_whitespace(text: str) -> str:
    return re.sub(r"[ \t]+", " ", re.sub(r"\n{3,}", "\n\n", text)).strip()


SAMPLE = """Hello support,

my order ORD-2026-00417 arrived broken broken. I paid €1.234,56 on 03.04.2026 and
another 49.90 EUR for shipping (invoice inv 2026 00999).   Please call +49 170 1234567
or write to ada.lovelace@example.com.  Reference code: Ticket-2026X.


Thanks! Ada"""


def main() -> None:
    print("Day 81 – Support ticket parser\n")
    print("orders :", [str(o) for o in find_orders(SAMPLE)])
    print("amounts:", parse_amounts(SAMPLE))
    print("dates  :", parse_dates(SAMPLE + " Delivered 2026-04-05."))
    print("repeats:", find_repeated_words(SAMPLE))
    print("strong reference 'Ticket-2026X'?", is_strong_reference("Ticket-2026X"))
    print("valid 'ORD-2026-00417'?", valid_order_number("ORD-2026-00417"), "| 'x ORD-2026-00417'?",
          valid_order_number("x ORD-2026-00417"))
    print("\nredacted:\n" + redact(normalise_whitespace(SAMPLE)))
    print("\nsentences:", split_sentences("It broke. Can you help? Thanks!"))


if __name__ == "__main__":
    main()
