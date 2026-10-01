"""Tests for Day 82 – SQLite."""

import sqlite3
from datetime import date

import pytest

from src.day_82_sqlite_database.main import (
    MIGRATIONS,
    GymError,
    add_member,
    check_in,
    connect,
    find_member,
    import_members,
    main,
    migrate,
    open_db,
    query_plan,
    sell_pass,
    unsafe_find_member,
    visits_report,
)


@pytest.fixture
def db():
    with open_db() as conn:
        yield conn


def test_migrations_are_versioned_and_idempotent(tmp_path):
    path = tmp_path / "gym.db"
    with open_db(path) as conn:
        assert conn.execute("PRAGMA user_version").fetchone()[0] == len(MIGRATIONS)
    with open_db(path) as conn:  # reopening applies nothing new
        assert migrate(conn) == len(MIGRATIONS)
        columns = [row["name"] for row in conn.execute("PRAGMA table_info(member)")]
    assert "wallet_cents" in columns


def test_migrate_upgrades_an_old_database(tmp_path):
    conn = connect(tmp_path / "old.db")
    conn.executescript(MIGRATIONS[0] + "; PRAGMA user_version = 1;")
    conn.execute("INSERT INTO member (email, name, joined_on) VALUES ('a@b.co', 'A', '2026-01-01')")
    conn.commit()
    assert migrate(conn) == 2
    assert find_member(conn, "a@b.co").wallet_cents == 0  # existing rows get the default
    conn.close()


def test_open_db_closes_connection():
    with open_db() as conn:
        pass
    with pytest.raises(sqlite3.ProgrammingError):
        conn.execute("SELECT 1")


@pytest.mark.parametrize(("email", "name"), [("bad-email", "X"), ("x@y.com", "   ")])
def test_constraints_reject_bad_rows(db, email, name):
    with pytest.raises(GymError):
        add_member(db, email, name)


def test_unique_email_case_insensitive(db):
    add_member(db, "Ada@Example.com", "Ada")
    with pytest.raises(GymError, match="UNIQUE"):
        add_member(db, "ada@example.com", "Ada again")


def test_executemany_is_all_or_nothing(db):
    assert import_members(db, [("a@x.io", "A"), ("b@x.io", "B")]) == 2
    with pytest.raises(sqlite3.IntegrityError):
        import_members(db, [("c@x.io", "C"), ("a@x.io", "duplicate")])
    assert find_member(db, "c@x.io") is None  # rolled back with the bad row


def test_transaction_rolls_back_both_statements(db):
    member = add_member(db, "g@x.io", "Grace", wallet_cents=1_000)
    with pytest.raises(GymError, match="rolled back"):
        sell_pass(db, member, visits=5, price_cents=5_000)  # wallet would go negative
    assert find_member(db, "g@x.io").wallet_cents == 1_000
    assert db.execute("SELECT COUNT(*) FROM pass").fetchone()[0] == 0


def test_foreign_keys_enforced(db):
    with pytest.raises(GymError):
        sell_pass(db, member_id=999, visits=1, price_cents=1)


def test_check_in_until_empty(db):
    member = add_member(db, "a@x.io", "A", wallet_cents=5_000)
    pass_id = sell_pass(db, member, visits=2, price_cents=1_000)
    assert check_in(db, pass_id, date(2026, 1, 1)) == 1
    assert check_in(db, pass_id, date(2026, 1, 2)) == 0
    with pytest.raises(GymError, match="empty"):
        check_in(db, pass_id, date(2026, 1, 3))


def test_parameterised_query_blocks_injection(db):
    add_member(db, "a@x.io", "Alice")
    add_member(db, "b@x.io", "Bob")
    attack = "' OR '1'='1"
    assert sorted(unsafe_find_member(db, attack)) == ["Alice", "Bob"]  # leaks every row
    assert find_member(db, attack) is None


def test_report_and_index_usage(db):
    a = add_member(db, "a@x.io", "Ann", wallet_cents=9_000)
    add_member(db, "b@x.io", "Ben")
    pass_id = sell_pass(db, a, visits=3, price_cents=3_000)
    check_in(db, pass_id, date(2026, 1, 1))
    assert visits_report(db) == [{"name": "Ann", "visits": 1, "remaining": 2},
                                 {"name": "Ben", "visits": 0, "remaining": 0}]
    assert "idx_checkin_day" in query_plan(db, "2026-01-01")


def test_main(capsys):
    main()
    out = capsys.readouterr().out
    assert "rolled back:" in out and "safe: None" in out
