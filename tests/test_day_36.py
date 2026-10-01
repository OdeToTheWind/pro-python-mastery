"""Tests for Day 36 – Instances and State."""

import gc

import pytest

from src.day_36_python_instances_and_state.main import InvalidTransition, Order, main


def test_instances_have_independent_state():
    a, b = Order("A", ["x"]), Order("B", ["y"])
    a.advance("cooking")
    assert (a.state, b.state) == ("cooking", "placed")
    assert a.id != b.id
    a.items.append("z")
    assert b.items == ["y"]
    a.close(), b.close()


def test_order_requires_items():
    with pytest.raises(ValueError):
        Order("A", [])


def test_valid_lifecycle_and_history():
    order = Order("A", ["x"])
    for state in ("cooking", "out_for_delivery", "delivered"):
        order.advance(state, note=state)
    assert order.is_final
    assert [s for s, _ in order.history] == ["placed", "cooking", "out_for_delivery", "delivered"]
    order.close()


@pytest.mark.parametrize(("path", "bad"), [((), "delivered"), (("cooking", "out_for_delivery"), "cancelled")])
def test_invalid_transitions(path, bad):
    order = Order("A", ["x"])
    for state in path:
        order.advance(state)
    with pytest.raises(InvalidTransition):
        order.advance(bad)
    order.close()


def test_snapshot_and_restore():
    order = Order("A", ["x"])
    snap = order.snapshot()
    order.advance("cooking")
    order.items.append("y")
    order.restore(snap)
    assert (order.state, order.items) == ("placed", ["x"])
    other = Order("B", ["z"])
    with pytest.raises(ValueError):
        other.restore(snap)
    order.close(), other.close()


def test_class_variable_tracks_open_orders_and_close_is_idempotent():
    start = Order.open_orders
    order = Order("A", ["x"])
    assert Order.open_orders == start + 1
    order.close()
    order.close()
    assert Order.open_orders == start
    with pytest.raises(InvalidTransition):
        order.advance("cooking")


def test_context_manager_cancels_on_error():
    with pytest.raises(RuntimeError), Order("A", ["x"]) as order:
        raise RuntimeError("boom")
    assert order.state == "cancelled" and order.closed
    assert order.history[-1] == ("cancelled", "error: boom")


def test_finalizer_runs_on_garbage_collection():
    order = Order("A", ["x"])
    order_id = order.id
    order.close()
    del order
    gc.collect()
    assert order_id in Order.finalized


def test_main(capsys):
    main()
    out = capsys.readouterr().out
    assert "Refused: cannot go from placed to delivered" in out
    assert "after error: cancelled" in out
