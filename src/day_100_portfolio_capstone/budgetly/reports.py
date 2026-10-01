"""Pure functions over expenses – the easiest code in the project to test."""

from __future__ import annotations

import csv
import io
from collections import defaultdict
from dataclasses import dataclass
from decimal import Decimal

from .models import Expense


@dataclass(frozen=True)
class CategoryLine:
    category: str
    spent: Decimal
    budget: Decimal | None

    @property
    def over_budget(self) -> bool:
        return self.budget is not None and self.spent > self.budget


def summarise(expenses: list[Expense], budgets: dict[str, Decimal]) -> list[CategoryLine]:
    totals: dict[str, Decimal] = defaultdict(Decimal)
    for e in expenses:
        totals[e.category] += e.amount
    names = sorted(set(totals) | set(budgets))
    return [CategoryLine(n, totals.get(n, Decimal("0")), budgets.get(n)) for n in names]


def render_table(lines: list[CategoryLine], currency: str) -> str:
    if not lines:
        return "no expenses yet"
    rows = [f"{'category':<10} {'spent':>10} {'budget':>10}"]
    for ln in lines:
        budget = f"{ln.budget:.2f}" if ln.budget is not None else "-"
        rows.append(f"{ln.category:<10} {ln.spent:>10.2f} {budget:>10}{'  ⚠ over' if ln.over_budget else ''}")
    total = sum((ln.spent for ln in lines), Decimal("0"))
    rows.append(f"{'total':<10} {total:>10.2f} {currency}")
    return "\n".join(rows)


def to_csv(expenses: list[Expense]) -> str:
    buffer = io.StringIO()
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(["id", "date", "amount", "category", "note"])
    for e in expenses:
        note = "'" + e.note if e.note[:1] in {"=", "+", "-", "@"} else e.note  # formula-injection guard
        writer.writerow([e.id, e.spent_on.isoformat(), f"{e.amount:.2f}", e.category, note])
    return buffer.getvalue()
