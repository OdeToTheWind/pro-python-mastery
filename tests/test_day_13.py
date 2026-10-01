"""Tests for Day 13 – For Loops."""

import pytest

from src.day_13_for_loops.main import (
    first_disqualified,
    heat_table,
    lane_numbers,
    main,
    multiplication_table,
    pair_results,
    ranking_board,
)


def test_lane_numbers_range_semantics():
    assert lane_numbers(1, 5) == [1, 2, 3, 4]
    assert lane_numbers(8, 0, -2) == [8, 6, 4, 2]
    assert lane_numbers(5, 1) == []


def test_lane_numbers_zero_step():
    with pytest.raises(ValueError):
        lane_numbers(1, 5, 0)


def test_pair_results_strict_zip():
    assert pair_results(["a", "b"], [1.0, 2.0]) == [("a", 1.0), ("b", 2.0)]
    with pytest.raises(ValueError):
        pair_results(["a", "b"], [1.0])


def test_ranking_board_ties_share_place():
    board = ranking_board([("Asha", 12.4), ("Ben", 11.9), ("Chen", 12.4), ("Dara", 13.8)])
    assert [line.split()[0] for line in board] == ["1.", "2.", "2.", "4."]
    assert board[0] == " 1. Ben         11.90s"


def test_heat_table_nested():
    table = heat_table(2, 3)
    assert table == [["H1-L1", "H1-L2", "H1-L3"], ["H2-L1", "H2-L2", "H2-L3"]]
    assert heat_table(0, 3) == []


def test_multiplication_table():
    lines = multiplication_table(3).splitlines()
    assert lines == [" 1 2 3", " 2 4 6", " 3 6 9"]
    assert multiplication_table(4).splitlines()[-1] == "  4  8 12 16"


def test_for_else_with_and_without_break():
    results = [("a", 10.0), ("b", 14.0), ("c", 15.0)]
    assert first_disqualified(results, 13.0) == "b exceeded the 13.0s limit"
    assert first_disqualified(results, 20.0) == "everyone finished within the limit"
    assert first_disqualified([], 1.0) == "everyone finished within the limit"


def test_main(capsys):
    main()
    assert "Dara exceeded the 13.0s limit" in capsys.readouterr().out
