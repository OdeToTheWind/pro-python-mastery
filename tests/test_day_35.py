"""Tests for Day 35 – Event Listeners."""

from src.day_35_event_listeners.main import Doorbell, EventBus, build_home, main


def test_emit_calls_every_listener_with_payload():
    bus, seen = EventBus(), []
    bus.on("motion", lambda room: seen.append(("a", room)))
    bus.on("motion", lambda room: seen.append(("b", room)))
    bus.emit("motion", room="hall")
    assert seen == [("a", "hall"), ("b", "hall")]


def test_emit_without_listeners():
    assert EventBus().emit("nothing") == []


def test_priority_order():
    bus, order = EventBus(), []
    bus.on("e", lambda: order.append("low"), priority=1)
    bus.on("e", lambda: order.append("high"), priority=9)
    bus.emit("e")
    assert order == ["high", "low"]


def test_off_and_unsubscribe_handle():
    bus = EventBus()

    def cb():
        return 1

    unsubscribe = bus.on("e", cb)
    unsubscribe()
    assert bus.listener_count("e") == 0
    assert bus.off("e", cb) is False


def test_once_runs_a_single_time():
    bus, calls = EventBus(), []
    bus.once("e", lambda: calls.append(1))
    bus.emit("e")
    bus.emit("e")
    assert calls == [1]


def test_decorator_registration_returns_function():
    bus = EventBus()

    @bus.listener("e")
    def handler():
        return "handled"

    assert handler() == "handled"
    assert bus.emit("e") == ["handled"]


def test_failing_listener_is_isolated():
    bus = EventBus()
    bus.on("e", lambda: 1 / 0)
    bus.on("e", lambda: "still runs")
    assert bus.emit("e") == ["still runs"]
    assert "division by zero" in bus.errors[0]


def test_device_is_decoupled_from_listeners():
    bus = EventBus()
    bell = Doorbell(bus, "back door")
    assert bell.press("cat") == []
    bus.on("doorbell", lambda location, visitor: f"{visitor}@{location}")
    assert bell.press("cat") == ["cat@back door"]


def test_build_home_scenario():
    log = []
    bus, bell = build_home(log)
    assert bell.press("courier") == ["light", "phone", "badge"]
    assert bell.press("friend") == ["light", "phone"]
    assert log[:3] == ["light on at front door", "phone: courier is at the front door",
                       "first-visitor badge"]


def test_main(capsys):
    main()
    assert "faulty listener added" in capsys.readouterr().out
