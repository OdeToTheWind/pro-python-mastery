"""Day 43 – Reading and Writing to CSV.

Scenario: a *household expense tracker* that imports a bank CSV export,
validates each row, reports bad rows instead of crashing, and exports a
category summary.

Deliverables (syllabus):
* CSV processing (``csv.DictReader`` / ``csv.DictWriter``)
* Tabular data import / export
* Parsing and validating fields (dates, money, quoting, dialect sniffing)
"""

from __future__ import annotations

import csv
import io
from collections import defaultdict
from dataclasses import dataclass
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path

DELIVERABLES: dict[str, str] = {
    "reading CSV into dicts": "parse_expenses",
    "validation of each row": "parse_row",
    "writing CSV (DictWriter)": "write_expenses",
    "export of aggregated data": "export_summary",
    "dialect (delimiter) detection": "detect_delimiter",
}

FIELDS = ["date", "description", "category", "amount"]


@dataclass(frozen=True, slots=True)
class Expense:
    day: date
    description: str
    category: str
    amount: Decimal


def parse_row(row: dict[str, str]) -> Expense:
    missing = [f for f in FIELDS if not (row.get(f) or "").strip()]
    if missing:
        raise ValueError(f"missing {', '.join(missing)}")
    try:
        amount = Decimal(row["amount"].replace(",", ""))
    except InvalidOperation:
        raise ValueError(f"bad amount {row['amount']!r}") from None
    if amount <= 0:
        raise ValueError("amount must be positive")
    return Expense(date.fromisoformat(row["date"].strip()), row["description"].strip(),
                   row["category"].strip().lower(), amount)


def detect_delimiter(text: str) -> str:
    """Let ``csv.Sniffer`` pick the delimiter from the header line.

    Only the delimiter is taken from the sniffer: from a single line it cannot
    reliably infer quoting rules, so standard (Excel) quoting is kept.
    """
    header = text.splitlines()[0] if text.strip() else ""
    try:
        return csv.Sniffer().sniff(header, delimiters=",;\t").delimiter
    except csv.Error:
        return ","


def parse_expenses(text: str) -> tuple[list[Expense], list[str]]:
    """Return (valid expenses, error messages). Detects ``,`` vs ``;`` exports."""
    reader = csv.DictReader(io.StringIO(text, newline=""), delimiter=detect_delimiter(text))
    if reader.fieldnames is None or set(FIELDS) - set(reader.fieldnames):
        raise ValueError(f"CSV header must contain {FIELDS}")
    expenses, errors = [], []
    for line_number, row in enumerate(reader, start=2):  # line 1 is the header
        try:
            expenses.append(parse_row(row))
        except ValueError as exc:
            errors.append(f"line {line_number}: {exc}")
    return expenses, errors


def read_expenses(path: Path) -> tuple[list[Expense], list[str]]:
    return parse_expenses(path.read_text(encoding="utf-8-sig"))  # tolerate Excel's BOM


def write_expenses(path: Path, expenses: list[Expense]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as handle:  # newline="" is required by csv
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        for e in expenses:
            writer.writerow({"date": e.day.isoformat(), "description": e.description,
                             "category": e.category, "amount": f"{e.amount:.2f}"})


def totals_by_category(expenses: list[Expense]) -> dict[str, Decimal]:
    totals: defaultdict[str, Decimal] = defaultdict(Decimal)
    for e in expenses:
        totals[e.category] += e.amount
    return dict(sorted(totals.items(), key=lambda kv: kv[1], reverse=True))


def export_summary(path: Path, expenses: list[Expense]) -> None:
    grand = sum((e.amount for e in expenses), Decimal("0"))
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["category", "total", "share"])
        for category, total in totals_by_category(expenses).items():
            writer.writerow([category, f"{total:.2f}", f"{total / grand:.1%}" if grand else "0.0%"])


SAMPLE = """date;description;category;amount
2026-04-01;"Groceries; weekly";Food;82.40
2026-04-03;Bus pass;Transport;45.00
2026-04-04;Cinema;Fun;not-a-number
2026-04-05;"Dinner, ""La Piazza\"\"";Food;1,034.50
2026-04-06;;Fun;12
"""


def main(folder: Path | None = None) -> None:
    import tempfile

    print("Day 43 – Expense tracker\n")
    expenses, errors = parse_expenses(SAMPLE)
    for e in expenses:
        print(f"{e.day}  {e.description:<22} {e.category:<10} {e.amount:>9}")
    print("Skipped:", errors)
    with tempfile.TemporaryDirectory() as tmp:
        out_dir = folder or Path(tmp)
        write_expenses(out_dir / "clean.csv", expenses)
        export_summary(out_dir / "summary.csv", expenses)
        print("\nsummary.csv:\n" + (out_dir / "summary.csv").read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
