"""Day 92 – Capstone: Test Suite for a Multi-module Package.

Scenario: ``lending`` – a *community library lending system* split into
``models``, ``repository``, ``notifier`` and ``service`` modules. The point of
the day is the **test suite**: factory fixtures, a fake repository, mocked
notifications, a frozen clock, parametrised business rules and a CI command
that enforces >90 % branch coverage for the package.

Deliverables (syllabus):
* A multi-module package designed for testing (dependency injection, Protocols)
* Fixtures (factories, ``tmp_path`` persistence, shared setup)
* Mocks (``unittest.mock.create_autospec``, ``side_effect``, ``caplog``)
* High coverage and a CI-friendly structure (one deterministic command)
"""

from __future__ import annotations

from datetime import date, timedelta

from .lending import (
    Book,
    InMemoryRepository,
    JsonRepository,
    LendingError,
    LendingService,
    Member,
    OutboxNotifier,
    models,
    notifier,
    repository,
    service,
)

DELIVERABLES: dict[str, str] = {
    "models module (rules on single objects)": "models.Loan.fine",
    "repository module (Protocol + JSON storage)": "repository.JsonRepository",
    "notifier module (mockable side effects)": "notifier.Notifier",
    "service module (injected dependencies)": "service.LendingService",
    "CI command with coverage gate": "CI_COMMAND",
}

CI_COMMAND = ("pytest tests/test_day_92.py --cov=src/day_92_multi_module_test_suite/lending "
              "--cov-branch --cov-fail-under=90 -q")

__all__ = ["CI_COMMAND", "DELIVERABLES", "Book", "InMemoryRepository", "JsonRepository", "LendingError",
           "LendingService", "Member", "OutboxNotifier", "main", "models", "notifier", "repository", "service"]


def main() -> None:
    print("Day 92 – Library lending package (run its tests with:)")
    print(" ", CI_COMMAND, "\n")
    clock = [date(2026, 9, 1)]
    outbox = OutboxNotifier()
    svc = LendingService(InMemoryRepository(), outbox, today=lambda: clock[0])
    svc.add_book(Book("978-0-306-40615-7", "Signals and Systems"))
    svc.join(Member("m1", "Ada", "ada@example.org"))
    loan = svc.borrow("m1", "9780306406157")
    print("due:", loan.due)
    clock[0] += timedelta(days=30)
    print("reminders sent:", svc.send_overdue_reminders(), outbox.outbox[0][1])
    print("fine on return: €", svc.give_back("m1", "9780306406157"), sep="")
    try:
        svc.borrow("m1", "0000000000000")
    except LendingError as exc:
        print("refused:", exc)


if __name__ == "__main__":
    main()
