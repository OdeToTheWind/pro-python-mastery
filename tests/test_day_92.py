"""Tests for Day 92 – the ``lending`` package (fixtures, fakes, mocks, frozen clock)."""

import logging
from datetime import date, timedelta
from decimal import Decimal
from unittest.mock import create_autospec

import pytest

from src.day_92_multi_module_test_suite.lending import (
    Book,
    InMemoryRepository,
    JsonRepository,
    LendingError,
    LendingService,
    Loan,
    Member,
    OutboxNotifier,
)
from src.day_92_multi_module_test_suite.lending.notifier import Notifier
from src.day_92_multi_module_test_suite.main import CI_COMMAND, main

ISBN = "9780306406157"
OTHER = "9781861972712"
START = date(2026, 9, 1)


class Clock:
    def __init__(self, today=START):
        self.today = today

    def __call__(self):
        return self.today

    def advance(self, days):
        self.today += timedelta(days=days)


@pytest.fixture
def clock():
    return Clock()


@pytest.fixture
def mailer():
    return create_autospec(Notifier, instance=True)  # fails if the call signature drifts


@pytest.fixture
def make_service(clock, mailer):
    def factory(repo=None, copies=1, members=("m1",)):
        svc = LendingService(repo or InMemoryRepository(), mailer, today=clock)
        svc.add_book(Book(ISBN, "Signals", copies=copies))
        svc.add_book(Book(OTHER, "Gödel", copies=1))
        for mid in members:
            svc.join(Member(mid, mid.upper(), f"{mid}@lib.org", max_loans=2))
        return svc

    return factory


@pytest.mark.parametrize("isbn", ["978-0-306-40615-7", "9781861972712"])
def test_valid_isbn_normalised(isbn):
    assert Book(isbn, "t").isbn.isdigit()


@pytest.mark.parametrize(("isbn", "message"), [("123", "invalid"), ("9780306406158", "checksum")])
def test_invalid_isbn(isbn, message):
    with pytest.raises(LendingError, match=message):
        Book(isbn, "t")


@pytest.mark.parametrize(("days_late", "fine"), [(0, "0"), (1, "0.25"), (8, "2.00"), (100, "10.00")])
def test_fine_is_capped(days_late, fine):
    loan = Loan(ISBN, "m1", START)
    assert loan.fine(loan.due + timedelta(days=days_late)) == Decimal(fine)


def test_renewals_extend_due_date_twice_only():
    loan = Loan(ISBN, "m1", START)
    loan.renew()
    loan.renew()
    assert loan.due == START + timedelta(days=63)
    with pytest.raises(LendingError, match="at most twice"):
        loan.renew()
    assert Loan(ISBN, "m1", START, renewals=1).due == START + timedelta(days=42)


def test_borrow_and_return_on_time(make_service, clock):
    svc = make_service()
    loan = svc.borrow("m1", ISBN)
    assert loan.due == date(2026, 9, 22) and svc.available(ISBN) == 0
    clock.advance(10)
    assert svc.give_back("m1", ISBN) == 0 and svc.available(ISBN) == 1


@pytest.mark.parametrize(
    ("setup", "member", "isbn", "message"),
    [(lambda s: None, "ghost", ISBN, "unknown member"),
     (lambda s: None, "m1", "9791234567896", "unknown book"),
     (lambda s: s.borrow("m2", ISBN), "m1", ISBN, "no copies"),
     (lambda s: (s.borrow("m1", ISBN), s.borrow("m1", OTHER)), "m1", ISBN, "limit of 2")],
)
def test_borrow_rules(make_service, setup, member, isbn, message):
    svc = make_service(members=("m1", "m2"))
    setup(svc)
    with pytest.raises(LendingError, match=message):
        svc.borrow(member, isbn)


def test_fines_block_new_loans_until_returned(make_service, clock):
    svc = make_service(copies=2)
    svc.borrow("m1", ISBN)
    clock.advance(25)  # 4 days late
    assert svc.outstanding_fines("m1") == Decimal("1.00")
    with pytest.raises(LendingError, match="fines"):
        svc.borrow("m1", OTHER)
    assert svc.give_back("m1", ISBN) == Decimal("1.00")
    with pytest.raises(LendingError, match="no such open loan"):
        svc.give_back("m1", ISBN)


def test_duplicate_member_and_extra_copies(make_service):
    svc = make_service()
    svc.add_book(Book(ISBN, "Signals", copies=2))
    assert svc.available(ISBN) == 3
    with pytest.raises(LendingError, match="already exists"):
        svc.join(Member("m1", "x", "x@y.z"))


def test_reminders_use_the_notifier(make_service, clock, mailer):
    svc = make_service(members=("m1", "m2"))
    svc.borrow("m1", ISBN)
    svc.borrow("m2", OTHER)
    clock.advance(21)
    assert svc.send_overdue_reminders() == 0  # due today is not overdue
    clock.advance(1)
    assert svc.send_overdue_reminders() == 2
    mailer.send.assert_any_call("m1@lib.org", "Overdue: Signals",
                                "Hi M1, 'Signals' was due 2026-09-22. Fine so far: €0.25.")


def test_one_failing_reminder_does_not_stop_others(make_service, clock, mailer, caplog):
    mailer.send.side_effect = [ConnectionError("smtp down"), None]
    svc = make_service(members=("m1", "m2"))
    svc.borrow("m1", ISBN)
    svc.borrow("m2", OTHER)
    clock.advance(30)
    with caplog.at_level(logging.ERROR, logger="lending"):
        assert svc.send_overdue_reminders() == 1
    assert "could not remind m1" in caplog.text and mailer.send.call_count == 2


def test_json_repository_round_trip(make_service, tmp_path, clock):
    path = tmp_path / "data" / "library.json"
    svc = make_service(repo=JsonRepository(path))
    svc.borrow("m1", ISBN)
    clock.advance(3)
    svc.give_back("m1", ISBN)
    svc.borrow("m1", OTHER)
    reloaded = JsonRepository(path)
    assert reloaded.books[ISBN].title == "Signals" and reloaded.members["m1"].max_loans == 2
    assert [(ln.isbn, ln.returned) for ln in reloaded.loans] == [(ISBN, date(2026, 9, 4)), (OTHER, None)]
    assert reloaded.loans[1].due == date(2026, 9, 25) and reloaded.saves == 0


def test_outbox_notifier_validates_address():
    outbox = OutboxNotifier()
    outbox.send("a@b.c", "s", "b")
    with pytest.raises(ValueError, match="cannot send"):
        outbox.send("nobody", "s", "b")
    assert outbox.outbox == [("a@b.c", "s", "b")]


def test_ci_command_and_main(capsys):
    assert "--cov-fail-under=90" in CI_COMMAND and "--cov-branch" in CI_COMMAND
    main()
    out = capsys.readouterr().out
    assert "fine on return: €2.25" in out and "refused: unknown book" in out
