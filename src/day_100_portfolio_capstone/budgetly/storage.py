"""SQLite repository: parameterised SQL, versioned schema, transactions."""

from __future__ import annotations

import logging
import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from datetime import date
from decimal import Decimal
from pathlib import Path

from .models import Expense

log = logging.getLogger("budgetly.storage")

MIGRATIONS = [
    """CREATE TABLE expense (
           id INTEGER PRIMARY KEY,
           spent_on TEXT NOT NULL,
           cents INTEGER NOT NULL CHECK (cents > 0),
           category TEXT NOT NULL,
           note TEXT NOT NULL DEFAULT '')""",
    "CREATE INDEX idx_expense_month ON expense (spent_on)",
]


@contextmanager
def open_store(path: Path | str) -> Iterator[Store]:
    if str(path) != ":memory:":
        Path(path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    try:
        store = Store(conn)
        store.migrate()
        yield store
    finally:
        conn.close()


class Store:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    def migrate(self) -> int:
        version = self.conn.execute("PRAGMA user_version").fetchone()[0]
        for number, sql in enumerate(MIGRATIONS[version:], start=version + 1):
            with self.conn:
                self.conn.execute(sql)
                self.conn.execute(f"PRAGMA user_version = {number}")
            log.debug("applied migration %d", number)
        return len(MIGRATIONS)

    def add(self, expense: Expense) -> int:
        with self.conn:
            cur = self.conn.execute(
                "INSERT INTO expense (spent_on, cents, category, note) VALUES (?, ?, ?, ?)",
                (expense.spent_on.isoformat(), int(expense.amount * 100), expense.category, expense.note))
        log.info("stored expense %s", cur.lastrowid)
        return int(cur.lastrowid or 0)

    def delete(self, expense_id: int) -> bool:
        with self.conn:
            return self.conn.execute("DELETE FROM expense WHERE id = ?", (expense_id,)).rowcount == 1

    def month(self, year: int, month: int) -> list[Expense]:
        prefix = f"{year:04d}-{month:02d}-%"
        rows = self.conn.execute("SELECT id, spent_on, cents, category, note FROM expense "
                                 "WHERE spent_on LIKE ? ORDER BY spent_on, id", (prefix,))
        return [Expense(date.fromisoformat(d), Decimal(c).scaleb(-2), cat, note, i) for i, d, c, cat, note in rows]
