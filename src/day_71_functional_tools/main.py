"""Day 71 – Functional Tools.

Scenario: a *music-streaming royalty calculator* – play logs are grouped,
accumulated and combined with ``itertools``; pricing rules are pre-configured
with ``partial``; expensive look-ups are cached with ``lru_cache``; totals are
folded with ``reduce``.

Deliverables (syllabus):
* ``itertools`` (groupby, accumulate, chain, pairwise, batched, combinations, islice)
* ``functools`` (partial, lru_cache, reduce, singledispatch, total_ordering, cache_info)
"""

from __future__ import annotations

import itertools
import operator
from collections.abc import Callable, Iterable, Iterator
from dataclasses import dataclass
from decimal import Decimal
from functools import lru_cache, partial, reduce, singledispatch, total_ordering

DELIVERABLES: dict[str, str] = {
    "itertools.groupby": "plays_per_artist",
    "itertools.accumulate": "running_streams",
    "itertools.chain / islice": "merge_playlists",
    "itertools.pairwise": "skip_detector",
    "itertools.batched": "payout_batches",
    "itertools.combinations": "collab_pairs",
    "functools.partial": "royalty_for",
    "functools.lru_cache": "artist_rate",
    "functools.reduce": "total_payout",
    "functools.singledispatch": "describe",
    "functools.total_ordering": "Track",
}


@dataclass(frozen=True, slots=True)
class Play:
    artist: str
    track: str
    seconds: int
    country: str


@total_ordering
@dataclass(frozen=True)
class Track:
    """Define ``__eq__`` and ``__lt__``; ``total_ordering`` fills in ``<= > >=``."""

    title: str
    streams: int

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Track):
            return NotImplemented
        return (self.streams, self.title) < (other.streams, other.title)


RATES = {"IN": Decimal("0.0008"), "DE": Decimal("0.0040"), "US": Decimal("0.0035")}
LOOKUPS: list[str] = []


@lru_cache(maxsize=128)
def artist_rate(artist: str, country: str) -> Decimal:
    """Pretend this hits a slow contracts database – the cache avoids repeated calls."""
    LOOKUPS.append(f"{artist}/{country}")
    bonus = Decimal("1.2") if artist.startswith("The ") else Decimal("1")
    return RATES.get(country, Decimal("0.0020")) * bonus


def royalty(play: Play, *, min_seconds: int, currency_rate: Decimal) -> Decimal:
    """A play counts only after *min_seconds*; amounts are converted to the payout currency."""
    if play.seconds < min_seconds:
        return Decimal("0")
    return artist_rate(play.artist, play.country) * currency_rate


# partial freezes keyword arguments: two specialised calculators from one function
royalty_for = {
    "EUR": partial(royalty, min_seconds=30, currency_rate=Decimal("1")),
    "INR": partial(royalty, min_seconds=30, currency_rate=Decimal("90")),
}


def total_payout(plays: Iterable[Play], calculator: Callable[[Play], Decimal]) -> Decimal:
    """``reduce`` folds a sequence into one value (``sum`` is usually clearer – both shown)."""
    return reduce(operator.add, map(calculator, plays), Decimal("0")).quantize(Decimal("0.0001"))


def plays_per_artist(plays: Iterable[Play]) -> dict[str, int]:
    """``groupby`` only groups *consecutive* items – sort by the same key first."""
    key = operator.attrgetter("artist")
    return {artist: sum(1 for _ in group) for artist, group in itertools.groupby(sorted(plays, key=key), key=key)}


def running_streams(daily: Iterable[int]) -> list[int]:
    return list(itertools.accumulate(daily))


def merge_playlists(*playlists: Iterable[str], limit: int | None = None) -> list[str]:
    """Chain several playlists lazily, de-duplicate, and optionally cut with islice."""
    unique = dict.fromkeys(itertools.chain.from_iterable(playlists))
    return list(itertools.islice(unique, limit))


def skip_detector(positions: Iterable[int]) -> list[tuple[int, int]]:
    """Consecutive playback positions that jump forward by more than 30 s."""
    return [(a, b) for a, b in itertools.pairwise(positions) if b - a > 30]


def payout_batches(artists: Iterable[str], size: int) -> list[tuple[str, ...]]:
    return list(itertools.batched(artists, size))


def collab_pairs(artists: Iterable[str]) -> list[tuple[str, str]]:
    return list(itertools.combinations(sorted(set(artists)), 2))


@singledispatch
def describe(value: object) -> str:
    return f"unknown: {value!r}"


@describe.register
def _(value: Play) -> str:
    return f"{value.artist} – {value.track} ({value.seconds}s, {value.country})"


@describe.register
def _(value: Track) -> str:
    return f"{value.title}: {value.streams:,} streams"


@describe.register(list)
def _(value: list[object]) -> str:
    return "; ".join(describe(v) for v in value)


def every_nth(iterable: Iterable[str], n: int) -> Iterator[str]:
    return itertools.islice(iterable, 0, None, n)


PLAYS = [
    Play("The Weeknd", "Blinding Lights", 200, "DE"),
    Play("Arijit Singh", "Tum Hi Ho", 260, "IN"),
    Play("The Weeknd", "Save Your Tears", 12, "US"),
    Play("Dua Lipa", "Levitating", 203, "US"),
    Play("Arijit Singh", "Kesariya", 268, "IN"),
    Play("The Weeknd", "Blinding Lights", 200, "DE"),
]


def main() -> None:
    print("Day 71 – Streaming royalties\n")
    print("plays per artist:", plays_per_artist(PLAYS))
    print("payout EUR:", total_payout(PLAYS, royalty_for["EUR"]), "| INR:", total_payout(PLAYS, royalty_for["INR"]))
    print("rate lookups:", len(LOOKUPS), "|", artist_rate.cache_info())
    print("running streams:", running_streams([120, 80, 200, 50]))
    print("merged:", merge_playlists(["a", "b"], ["b", "c"], ["d"], limit=3))
    print("skips:", skip_detector([0, 10, 70, 80, 200]))
    print("batches:", payout_batches(sorted(plays_per_artist(PLAYS)), 2))
    print("collabs:", collab_pairs(p.artist for p in PLAYS))
    print("top track:", max([Track("A", 10), Track("B", 50)]).title, "|", describe(PLAYS[0]))


if __name__ == "__main__":
    main()
