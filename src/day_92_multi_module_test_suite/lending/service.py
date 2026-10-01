"""Use cases: every dependency (repository, notifier, clock) is injected."""

from __future__ import annotations

import logging
from collections.abc import Callable
from datetime import date
from decimal import Decimal

from .models import Book, LendingError, Loan, Member
from .notifier import Notifier
from .repository import Repository

log = logging.getLogger("lending")


class LendingService:
    def __init__(self, repo: Repository, notifier: Notifier, today: Callable[[], date] = date.today) -> None:
        self.repo, self.notifier, self.today = repo, notifier, today

    def add_book(self, book: Book) -> None:
        existing = self.repo.books.get(book.isbn)
        if existing:
            existing.copies += book.copies
        else:
            self.repo.books[book.isbn] = book
        self.repo.save()

    def join(self, member: Member) -> None:
        if member.member_id in self.repo.members:
            raise LendingError(f"member {member.member_id} already exists")
        self.repo.members[member.member_id] = member
        self.repo.save()

    def open_loans(self, member_id: str | None = None, isbn: str | None = None) -> list[Loan]:
        return [ln for ln in self.repo.loans if ln.returned is None
                and member_id in (None, ln.member_id) and isbn in (None, ln.isbn)]

    def available(self, isbn: str) -> int:
        book = self.repo.books.get(isbn)
        if book is None:
            raise LendingError(f"unknown book {isbn}")
        return book.copies - len(self.open_loans(isbn=isbn))

    def borrow(self, member_id: str, isbn: str) -> Loan:
        member = self.repo.members.get(member_id)
        if member is None:
            raise LendingError(f"unknown member {member_id}")
        if self.outstanding_fines(member_id) > 0:
            raise LendingError("pay outstanding fines first")
        if len(self.open_loans(member_id)) >= member.max_loans:
            raise LendingError(f"limit of {member.max_loans} loans reached")
        if self.available(isbn) <= 0:
            raise LendingError("no copies available")
        loan = Loan(isbn, member_id, self.today())
        self.repo.loans.append(loan)
        self.repo.save()
        log.info("%s borrowed %s until %s", member_id, isbn, loan.due)
        return loan

    def give_back(self, member_id: str, isbn: str) -> Decimal:
        loans = self.open_loans(member_id, isbn)
        if not loans:
            raise LendingError("no such open loan")
        loan = loans[0]
        loan.returned = self.today()
        self.repo.save()
        return loan.fine(loan.returned)

    def outstanding_fines(self, member_id: str) -> Decimal:
        return sum((ln.fine(self.today()) for ln in self.repo.loans
                    if ln.member_id == member_id and ln.returned is None), Decimal("0"))

    def send_overdue_reminders(self) -> int:
        """Failures to notify one member must not stop the others."""
        sent = 0
        for loan in self.open_loans():
            if loan.due >= self.today():
                continue
            member = self.repo.members[loan.member_id]
            title = self.repo.books[loan.isbn].title
            try:
                self.notifier.send(member.email, f"Overdue: {title}",
                                   f"Hi {member.name}, '{title}' was due {loan.due}. "
                                   f"Fine so far: €{loan.fine(self.today())}.")
                sent += 1
            except Exception:
                log.exception("could not remind %s", member.member_id)
        return sent
