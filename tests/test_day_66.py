"""Tests for Day 66 – Advanced Generators."""

from decimal import Decimal

import pytest

from src.day_66_advanced_generators.main import (
    RAW,
    batched,
    build_pipeline,
    count_and_forward,
    main,
    parse_lines,
    revenue_tracker,
    valid_orders,
    walk_categories,
    with_tax,
)


def test_walk_categories_flattens_with_yield_from():
    tree = {"A": {"B": {"C": {}}}, "D": {}}
    assert list(walk_categories(tree)) == ["A", "A/B", "A/B/C", "D"]


def test_parse_lines_skips_comments_blank_and_broken():
    rows = list(parse_lines(RAW + ["", "   "]))
    assert [r["order_id"] for r in rows] == ["A1", "A2", "A3", "A4", "A5"]


def test_valid_orders_rejects_bad_quantity_and_country():
    rejected = []
    orders = list(valid_orders(parse_lines(RAW), rejected))
    assert [o.order_id for o in orders] == ["A1", "A2", "A5"]
    assert rejected == ["A3", "A4"]
    assert orders[1].country == "FR"


def test_with_tax():
    rejected = []
    taxed = dict((o.order_id, g) for o, g in with_tax(valid_orders(parse_lines(RAW), rejected)))
    assert taxed == {"A1": Decimal("29.75"), "A2": Decimal("23.99"), "A5": Decimal("94.35")}


def test_batched():
    assert list(batched(range(5), 2)) == [[0, 1], [2, 3], [4]]
    assert list(batched([], 3)) == []
    with pytest.raises(ValueError):
        list(batched([1], 0))


def test_pipeline_is_lazy():
    pulled = []

    def source():
        for line in RAW:
            pulled.append(line)
            yield line

    pipeline = build_pipeline(source(), [], batch_size=1)
    assert pulled == []
    first = next(pipeline)
    assert first[0][0].order_id == "A1"
    assert len(pulled) == 2  # only the comment and the first order were read


def test_pipeline_end_to_end():
    rejected = []
    batches = list(build_pipeline(RAW, rejected, batch_size=2))
    assert [len(b) for b in batches] == [2, 1]
    assert rejected == ["A3", "A4"]


def test_yield_from_captures_return_value():
    totals = []
    assert list(count_and_forward("abc", totals)) == ["a", "b", "c"]
    assert totals == [3]


def test_revenue_tracker_send():
    tracker = revenue_tracker()
    assert next(tracker)["count"] == 0
    tracker.send(Decimal("10"))
    stats = tracker.send(Decimal("5"))
    assert stats["total"] == Decimal("15") and stats["average"] == Decimal("7.50")


def test_revenue_tracker_must_be_primed():
    with pytest.raises(TypeError):
        revenue_tracker().send(Decimal("1"))


def test_revenue_tracker_throw_and_return_value():
    tracker = revenue_tracker()
    next(tracker)
    tracker.send(Decimal("2"))
    assert tracker.throw(ValueError("oops"))["errors"] == 1
    with pytest.raises(StopIteration) as info:
        tracker.send(None)
    assert info.value.value == Decimal("2")


def test_revenue_tracker_close():
    tracker = revenue_tracker()
    next(tracker)
    tracker.close()
    with pytest.raises(StopIteration):
        next(tracker)


def test_main(capsys):
    main()
    out = capsys.readouterr().out
    assert "rejected: ['A3', 'A4']" in out and "count returned: [3]" in out
