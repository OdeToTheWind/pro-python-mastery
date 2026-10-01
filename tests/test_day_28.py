"""Tests for Day 28 – Creating Classes."""

from datetime import date

import pytest

from src.day_28_classes.main import Book, main

TODAY = date(2026, 4, 9)


@pytest.fixture
def book():
    return Book("  Dune ", "Frank Herbert", "978-0-441-17271-9")


def test_init_sets_instance_attributes(book):
    assert (book.title, book.author, book.isbn) == ("Dune", "Frank Herbert", "9780441172719")
    assert book.available and book.borrower is None


@pytest.mark.parametrize(("title", "author", "isbn"), [("", "A", "9780441172719"),
                                                       ("T", "A", "123")])
def test_init_validation(title, author, isbn):
    with pytest.raises(ValueError):
        Book(title, author, isbn)


def test_class_attribute_counter_and_shared_constant(book):
    before = Book.copies_created
    other = Book("Emma", "Austen", "9780141439587")
    assert Book.copies_created == before + 1
    assert book.LOAN_DAYS == other.LOAN_DAYS == Book.LOAN_DAYS == 14


def test_check_out_and_return(book):
    assert book.check_out("Ravi", TODAY) == date(2026, 4, 23)
    assert not book.available
    with pytest.raises(RuntimeError):
        book.check_out("Ana", TODAY)
    book.return_book()
    assert book.available and book.due is None
    with pytest.raises(RuntimeError):
        book.return_book()


def test_days_overdue(book):
    assert book.days_overdue(TODAY) == 0
    book.check_out("Ravi", TODAY)
    assert book.days_overdue(date(2026, 4, 23)) == 0
    assert book.days_overdue(date(2026, 5, 1)) == 8


def test_dunder_methods(book):
    assert repr(book) == "Book(title='Dune', author='Frank Herbert', isbn='9780441172719')"
    assert str(book) == "Dune by Frank Herbert – available"
    book.check_out("Ravi", TODAY)
    assert str(book).endswith("due 23 Apr")
    twin = Book("Dune (copy)", "Herbert", "9780441172719")
    assert book == twin and len({book, twin}) == 1
    assert book != "Dune"


def test_main(capsys):
    main()
    assert "Overdue days on 1 May: 8" in capsys.readouterr().out
