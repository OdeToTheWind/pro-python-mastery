# Day 82 – SQLite & Pure Database Work Reflection

**Date:** 2026-10-01 · **Level:** Advanced · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_82_sqlite_database/main.py`](../../src/day_82_sqlite_database/main.py) · **Tests:** [`tests/test_day_82.py`](../../tests/test_day_82.py) (12 tests)

## Scenario
A *climbing-gym membership system* – members, passes and check-ins stored in SQLite with a proper schema, constraints, indexes, transactions and versioned migrations, using nothing but the standard library.

## Syllabus deliverables
> sqlite3, transactions, context managers, and basic schema design without an ORM

| Deliverable | Implemented in |
|---|---|
| ✅ schema design: keys, constraints, indexes | `MIGRATIONS` |
| ✅ versioned migrations (PRAGMA user\_version) | `migrate` |
| ✅ connection setup and Row factory | `connect` |
| ✅ context manager for a connection | `open_db` |
| ✅ parameterised queries (no SQL injection) | `find_member` |
| ✅ SQL injection demonstrated | `unsafe_find_member` |
| ✅ transactions with rollback | `sell_pass` |
| ✅ executemany bulk insert | `import_members` |
| ✅ aggregate queries with JOIN / GROUP BY | `visits_report` |

## Key learnings
- `sqlite3` with `?` placeholders makes SQL injection impossible – the unsafe f-string version leaks every row.
- `with conn:` wraps statements in a transaction: all succeed or everything rolls back.
- `PRAGMA user_version` gives simple, ordered schema migrations without an ORM.

## Pitfalls I hit (and how I fixed them)
- Foreign keys are off by default in SQLite – enable `PRAGMA foreign_keys = ON` on every connection.

## Run it
```bash
python -m src.day_82_sqlite_database.main
pytest tests/test_day_82.py -v
```

## Next step
- Build a robust command-line application on Day 83.
