"""Tests for Day 71 – Functional Tools."""

from decimal import Decimal
from functools import partial

import pytest

from src.day_71_functional_tools import main as day71
from src.day_71_functional_tools.main import (
    PLAYS,
    Play,
    Track,
    artist_rate,
    collab_pairs,
    describe,
    every_nth,
    merge_playlists,
    payout_batches,
    plays_per_artist,
    royalty_for,
    running_streams,
    skip_detector,
    total_payout,
)


@pytest.fixture(autouse=True)
def _fresh_cache():
    artist_rate.cache_clear()
    day71.LOOKUPS.clear()


def test_groupby_counts_after_sorting():
    assert plays_per_artist(PLAYS) == {"Arijit Singh": 2, "Dua Lipa": 1, "The Weeknd": 3}


def test_partial_freezes_keywords():
    eur = royalty_for["EUR"]
    assert isinstance(eur, partial) and eur.keywords["min_seconds"] == 30
    assert eur(Play("X", "t", 29, "US")) == 0
    assert eur(Play("X", "t", 30, "US")) == Decimal("0.0035")


def test_lru_cache_avoids_repeated_lookups():
    total_payout(PLAYS, royalty_for["EUR"])
    info = artist_rate.cache_info()
    # 6 plays, 5 long enough to count, but only 3 unique artist/country pairs
    assert len(day71.LOOKUPS) == 3
    assert info.hits == 2 and info.misses == 3


def test_reduce_total_matches_sum():
    calc = royalty_for["INR"]
    assert total_payout(PLAYS, calc) == sum((calc(p) for p in PLAYS), Decimal("0")).quantize(Decimal("0.0001"))
    assert total_payout([], calc) == 0


def test_accumulate():
    assert running_streams([1, 2, 3]) == [1, 3, 6]
    assert running_streams([]) == []


def test_chain_dedup_and_islice():
    assert merge_playlists(["a", "b"], ["b", "c"]) == ["a", "b", "c"]
    assert merge_playlists(["a", "b"], ["c"], limit=2) == ["a", "b"]


def test_pairwise_skip_detector():
    assert skip_detector([0, 10, 70, 80, 200]) == [(10, 70), (80, 200)]
    assert skip_detector([5]) == []


def test_batched_and_combinations():
    assert payout_batches("abcde", 2) == [("a", "b"), ("c", "d"), ("e",)]
    assert collab_pairs(["B", "A", "C", "A"]) == [("A", "B"), ("A", "C"), ("B", "C")]


def test_total_ordering():
    low, high = Track("A", 10), Track("B", 50)
    assert low < high and high >= low and low <= low and not low > high
    assert sorted([high, low]) == [low, high]


def test_singledispatch():
    assert describe(Track("Hit", 1500)) == "Hit: 1,500 streams"
    assert describe(PLAYS[0]).startswith("The Weeknd – Blinding Lights")
    assert describe([Track("A", 1), 5]) == "A: 1 streams; unknown: 5"


def test_every_nth():
    assert list(every_nth("abcdef", 2)) == ["a", "c", "e"]


def test_main(capsys):
    day71.main()
    assert "rate lookups: 3" in capsys.readouterr().out
