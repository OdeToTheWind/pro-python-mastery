"""Tests for Day 16 – Flowchart Programming."""

import itertools

import pytest

from src.day_16_flowchart_programming.main import (
    LOAN_CHART,
    Decision,
    loan_decision,
    main,
    overdue_fine,
    run_flowchart,
    sort_returns,
)


@pytest.mark.parametrize(
    ("active", "fines", "books_out", "expected"),
    [
        (False, 0, 0, "refuse: renew membership"),
        (True, 5.01, 0, "refuse: pay fines"),
        (True, 5, 5, "refuse: limit reached"),
        (True, 5, 4, "approve"),
    ],
)
def test_loan_decision(active, fines, books_out, expected):
    assert loan_decision(active=active, fines=fines, books_out=books_out) == expected


@pytest.mark.parametrize(("days", "fine"), [(0, 0), (1, 0), (2, 0.25), (7, 1.5), (8, 2.0), (100, 10.0)])
def test_overdue_fine_tiers(days, fine):
    assert overdue_fine(days) == fine


def test_overdue_fine_child_discount_and_validation():
    assert overdue_fine(8, is_child=True) == 1.0
    with pytest.raises(ValueError):
        overdue_fine(-1)


def test_sort_returns():
    assert sort_returns(["Dune", "SCI-Cosmos", "Emma!", "SCI-Genes!"]) == {
        "fiction": ["Dune"],
        "science": ["SCI-Cosmos"],
        "repair": ["Emma", "SCI-Genes"],
    }
    assert sort_returns([]) == {"fiction": [], "science": [], "repair": []}


@pytest.mark.parametrize(
    ("active", "owes", "under"), list(itertools.product([True, False], repeat=3))
)
def test_data_flowchart_matches_coded_version(active, owes, under):
    path = run_flowchart(LOAN_CHART, {"active": active, "owes_over_5": owes, "under_limit": under})
    coded = loan_decision(active=active, fines=10 if owes else 0, books_out=0 if under else 5)
    assert path[-1].lower() == coded


def test_flowchart_cycle_detection():
    chart = {"start": Decision("q", yes="start", no="start")}
    with pytest.raises(RuntimeError):
        run_flowchart(chart, {"q": True})


def test_main(capsys):
    main()
    assert "start → fines → limit → approve → APPROVE" in capsys.readouterr().out
