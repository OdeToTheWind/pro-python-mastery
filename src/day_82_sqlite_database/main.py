"""Day 82 – SQLite & Pure Database Work.

Scenario: a *climbing-gym membership system* – members, passes and check-ins
stored in SQLite with a proper schema, constraints, indexes, transactions and
versioned migrations, using nothing but the standard library.

Deliverables (syllabus):
* ``sqlite3`` (connections, cursors, ``Row`` factory, parameterised queries)
* Transactions (atomic multi-statement work, rollback on error)
* Context managers (``with conn:`` commits/rolls back; ``closing`` closes)
* Basic schema design without an ORM (keys, constraints, indexes, migrations)
"""

from __future__ import annotations

import contextlib
import sqlite3
from collections.abc import Iterator
from dataclasses import dataclass
from datetime import date
from pathlib import Path

DELIVERABLES: dict[str, str] = {
    "schema design: keys, constraints, indexes": "MIGRATIONS",
    "versioned migrations (PRAGMA user_version)": "migrate",
    "connection setup and Row factory": "connect",
    "context manager for a connection": "open_db",
    "parameterised queries (no SQL injection)": "find_member",
    "SQL injection demonstrated": "unsafe_find_member",
    "transactions with rollback": "sell_pass",
    "executemany bulk insert": "import_members",
    "aggregate queries with JOIN / GROUP BY": "visits_report",
}

MIGRATIONS: list[str] = [
    # v1 – initial schema
    """
    CREATE TABLE member (
        id INTEGER PRIMARY KEY,
        email TEXT NOT NULL UNIQUE CHECK (email LIKE '%_@_%.__%'),
        name TEXT NOT NULL CHECK (length(trim(name)) > 0),
        joined_on TEXT NOT NULL
    );
    CREATE TABLE pass (
        id INTEGER PRIMARY KEY,
        member_id INTEGER NOT NULL REFERENCES member(id) ON DELETE CASCADE,
        visits_left INTEGER NOT NULL CHECK (visits_left >= 0),
        price_cents INTEGER NOT NULL CHECK (price_cents > 0)
    );
    CREATE TABLE checkin (
        id INTEGER PRIMARY KEY,
        pass_id INTEGER NOT NULL REFERENCES pass(id) ON DELETE CASCADE,
        day TEXT NOT NULL
    );
    CREATE INDEX idx_checkin_day ON checkin(day);
    """,
    # v2 – a later feature: wallet balance per member
    "ALTER TABLE member ADD COLUMN wallet_cents INTEGER NOT NULL DEFAULT 0 CHECK (wallet_cents >= 0);",
]


class GymError(Exception):
    pass


@dataclass(frozen=True, slots=True)
class Member:
    id: int
    email: str
    name: str
    wallet_cents: int


def connect(path: str | Path = ":memory:") -> sqlite3.Connection:
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row  # rows behave like dicts and tuples
    conn.execute("PRAGMA foreign_keys = ON")  # off by default in SQLite!
    return conn


@contextlib.contextmanager
def open_db(path: str | Path = ":memory:") -> Iterator[sqlite3.Connection]:
    """``with conn:`` only manages the *transaction*; ``closing`` actually closes it."""
    with contextlib.closing(connect(path)) as conn:
        migrate(conn)
        yield conn


def migrate(conn: sqlite3.Connection) -> int:
    """Apply only the migrations newer than ``PRAGMA user_version``."""
    version = conn.execute("PRAGMA user_version").fetchone()[0]
    for number, script in enumerate(MIGRATIONS[version:], start=version + 1):
        with conn:
            conn.executescript(f"BEGIN; {script}; PRAGMA user_version = {number}; COMMIT;")
    return int(conn.execute("PRAGMA user_version").fetchone()[0])


def add_member(conn: sqlite3.Connection, email: str, name: str, wallet_cents: int = 0,
               joined: date | None = None) -> int:
    try:
        with conn:
            cursor = conn.execute(
                "INSERT INTO member (email, name, joined_on, wallet_cents) VALUES (?, ?, ?, ?)",
                (email.lower(), name, (joined or date.today()).isoformat(), wallet_cents),
            )
    except sqlite3.IntegrityError as exc:
        raise GymError(f"cannot add member {email!r}: {exc}") from exc
    return int(cursor.lastrowid or 0)


def import_members(conn: sqlite3.Connection, rows: list[tuple[str, str]]) -> int:
    """All or nothing: one bad row rolls back the whole batch."""
    with conn:
        conn.executemany("INSERT INTO member (email, name, joined_on) VALUES (?, ?, date('now'))",
                         [(email.lower(), name) for email, name in rows])
    return len(rows)


def find_member(conn: sqlite3.Connection, email: str) -> Member | None:
    """Placeholders (``?``) send data separately from SQL – injection is impossible."""
    row = conn.execute("SELECT id, email, name, wallet_cents FROM member WHERE email = ?",
                       (email.lower(),)).fetchone()
    return Member(**dict(row)) if row else None


def unsafe_find_member(conn: sqlite3.Connection, email: str) -> list[str]:
    """NEVER do this: string formatting lets input rewrite the query."""
    query = f"SELECT name FROM member WHERE email = '{email}'"  # noqa: S608 – deliberate demo
    return [row["name"] for row in conn.execute(query)]


def sell_pass(conn: sqlite3.Connection, member_id: int, visits: int, price_cents: int) -> int:
    """Debit the wallet *and* create the pass in one transaction."""
    try:
        with conn:  # BEGIN … COMMIT, or ROLLBACK if anything raises
            conn.execute("UPDATE member SET wallet_cents = wallet_cents - ? WHERE id = ?", (price_cents, member_id))
            cursor = conn.execute("INSERT INTO pass (member_id, visits_left, price_cents) VALUES (?, ?, ?)",
                                  (member_id, visits, price_cents))
    except sqlite3.IntegrityError as exc:
        raise GymError(f"sale failed and was rolled back: {exc}") from exc
    return int(cursor.lastrowid or 0)


def check_in(conn: sqlite3.Connection, pass_id: int, day: date) -> int:
    with conn:
        updated = conn.execute("UPDATE pass SET visits_left = visits_left - 1 WHERE id = ? AND visits_left > 0",
                               (pass_id,)).rowcount
        if updated == 0:
            raise GymError("pass is empty or does not exist")
        conn.execute("INSERT INTO checkin (pass_id, day) VALUES (?, ?)", (pass_id, day.isoformat()))
        return int(conn.execute("SELECT visits_left FROM pass WHERE id = ?", (pass_id,)).fetchone()[0])


def visits_report(conn: sqlite3.Connection) -> list[dict[str, object]]:
    rows = conn.execute(
        """
        SELECT m.name, COUNT(c.id) AS visits, COALESCE(SUM(p.visits_left), 0) AS remaining
        FROM member m
        LEFT JOIN pass p ON p.member_id = m.id
        LEFT JOIN checkin c ON c.pass_id = p.id
        GROUP BY m.id
        ORDER BY visits DESC, m.name
        """
    ).fetchall()
    return [dict(row) for row in rows]


def query_plan(conn: sqlite3.Connection, day: str) -> str:
    plan = conn.execute("EXPLAIN QUERY PLAN SELECT * FROM checkin WHERE day = ?", (day,)).fetchall()
    return " | ".join(row["detail"] for row in plan)


def main() -> None:
    print("Day 82 – Climbing gym database\n")
    with open_db() as conn:
        print("schema version:", conn.execute("PRAGMA user_version").fetchone()[0])
        ada = add_member(conn, "Ada@Example.com", "Ada", wallet_cents=10_000)
        add_member(conn, "grace@example.com", "Grace", wallet_cents=1_000)
        pass_id = sell_pass(conn, ada, visits=10, price_cents=8_000)
        for d in (1, 2, 3):
            check_in(conn, pass_id, date(2026, 10, d))
        try:
            sell_pass(conn, 2, visits=10, price_cents=8_000)
        except GymError as exc:
            print("rolled back:", exc)
        print("grace wallet still:", find_member(conn, "grace@example.com"))
        print("injection leaks:", unsafe_find_member(conn, "' OR '1'='1"), "| safe:", find_member(conn, "' OR '1'='1"))
        print("report:", visits_report(conn))
        print("plan:", query_plan(conn, "2026-10-01"))


if __name__ == "__main__":
    main()
