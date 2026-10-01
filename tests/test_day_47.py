"""Tests for Day 47 – Packing and Unpacking."""

import pytest

from src.day_47_packing_unpacking.main import (
    DEFAULT_SETTINGS,
    connect,
    join_routes,
    leg_distance,
    main,
    merge_settings,
    route_length,
    split_route,
    swap_ends,
    unzip,
)

LONDON, PARIS, BERLIN = (51.5074, -0.1278), (48.8566, 2.3522), (52.52, 13.405)


def test_star_unpacking_into_positional_parameters():
    assert leg_distance(*LONDON, *PARIS) == leg_distance(LONDON[0], LONDON[1], PARIS[0], PARIS[1]) == 343.6


def test_route_length_packs_any_number_of_points():
    assert route_length(LONDON) == 0
    assert route_length(LONDON, PARIS, BERLIN) == pytest.approx(343.6 + 877.5, abs=0.2)


def test_double_star_unpacking_into_keywords():
    settings = {"host": "h", "port": 1, "timeout": 2.0, "retries": 3}
    assert connect(**settings) == "h:1 (timeout 2.0s, retries=3)"
    assert connect("h", 1) == "h:1 (timeout 10.0s)"


def test_double_star_unpacking_reports_missing_argument():
    with pytest.raises(TypeError):
        connect(**{"host": "only-host"})


def test_extended_unpacking():
    assert split_route(["A", "B"]) == ("A", [], "B")
    assert split_route(["A", "B", "C", "D"]) == ("A", ["B", "C"], "D")
    with pytest.raises(ValueError):
        split_route(["A"])


def test_merge_settings_later_wins_and_defaults_untouched():
    merged = merge_settings({"port": 80}, {"port": 8080, "debug": True})
    assert merged == {"host": "maps.example.com", "port": 8080, "timeout": 5.0, "debug": True}
    assert DEFAULT_SETTINGS["port"] == 443


def test_join_routes():
    assert join_routes(["A", "B"], ["B", "C"]) == ["A", "B", "C"]
    assert join_routes(["A"], ["X", "Y"]) == ["A", "X", "Y"]
    assert join_routes([], ["X"]) == ["X"]


def test_unzip():
    assert unzip([("A", 1.0), ("B", 2.0)]) == (("A", "B"), (1.0, 2.0))
    assert unzip([]) == ((), ())


def test_swap_ends():
    route = ["A", "B", "C"]
    assert swap_ends(route) == ["C", "B", "A"]
    assert route == ["A", "B", "C"]


def test_main(capsys):
    main()
    assert "London → Paris: 343.6 km" in capsys.readouterr().out
