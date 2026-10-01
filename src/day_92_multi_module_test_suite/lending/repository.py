"""Storage behind a Protocol: tests use memory, production uses an atomic JSON file."""

from __future__ import annotations

import json
import os
import tempfile
from dataclasses import asdict
from datetime import date
from pathlib import Path
from typing import Protocol

from .models import Book, Loan, Member


class Repository(Protocol):
    books: dict[str, Book]
    members: dict[str, Member]
    loans: list[Loan]

    def save(self) -> None: ...


class InMemoryRepository:
    def __init__(self) -> None:
        self.books: dict[str, Book] = {}
        self.members: dict[str, Member] = {}
        self.loans: list[Loan] = []
        self.saves = 0

    def save(self) -> None:
        self.saves += 1


class JsonRepository(InMemoryRepository):
    def __init__(self, path: Path) -> None:
        super().__init__()
        self.path = path
        if path.exists():
            data = json.loads(path.read_text(encoding="utf-8"))
            self.books = {b["isbn"]: Book(**b) for b in data["books"]}
            self.members = {m["member_id"]: Member(**m) for m in data["members"]}
            for raw in data["loans"]:
                loan = Loan(raw["isbn"], raw["member_id"], date.fromisoformat(raw["borrowed"]),
                            date.fromisoformat(raw["returned"]) if raw["returned"] else None, raw["renewals"])
                self.loans.append(loan)

    def save(self) -> None:
        super().save()
        data = {"books": [asdict(b) for b in self.books.values()],
                "members": [asdict(m) for m in self.members.values()],
                "loans": [{**asdict(loan), "due": None} for loan in self.loans]}
        self.path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp = tempfile.mkstemp(dir=self.path.parent)
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(data, handle, default=str, indent=1)
        os.replace(tmp, self.path)
