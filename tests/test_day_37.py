"""Tests for Day 37 – Python Turtle (geometry tested with a fake pen, no window)."""

import math

import pytest

from src.day_37_python_turtle.main import (
    animate_orbit,
    draw_polygon,
    draw_spiral,
    draw_star,
    exterior_angle,
    move_to,
    orbit_positions,
    star_angle,
)


class FakePen:
    """Records every call so tests can assert on the drawing instructions."""

    def __init__(self):
        self.calls = []
        self.heading = 0.0

    def forward(self, distance):
        self.calls.append(("forward", distance))

    def right(self, angle):
        self.heading = (self.heading + angle) % 360
        self.calls.append(("right", angle))

    def penup(self):
        self.calls.append(("penup",))

    def pendown(self):
        self.calls.append(("pendown",))

    def goto(self, x, y):
        self.calls.append(("goto", x, y))

    def color(self, *args):
        self.calls.append(("color", *args))


@pytest.mark.parametrize(("sides", "angle"), [(3, 120), (4, 90), (6, 60)])
def test_exterior_angle(sides, angle):
    assert exterior_angle(sides) == angle


def test_polygon_validation():
    with pytest.raises(ValueError):
        exterior_angle(2)


def test_draw_polygon_closes_the_shape():
    pen = FakePen()
    assert draw_polygon(pen, 5, 10) == 360
    assert pen.calls.count(("forward", 10)) == 5
    assert math.isclose(pen.heading, 0, abs_tol=1e-9)


def test_star_angles():
    assert star_angle(5) == 144
    assert star_angle(7) == pytest.approx(154.2857, rel=1e-4)
    for bad in (4, 3):
        with pytest.raises(ValueError):
            star_angle(bad)


def test_draw_star_returns_to_heading():
    pen = FakePen()
    draw_star(pen, 5, 100)
    assert len(pen.calls) == 10
    assert math.isclose(pen.heading % 360, 0, abs_tol=1e-9)


def test_draw_spiral_growing_segments():
    pen = FakePen()
    assert draw_spiral(pen, 4, growth=2) == 20  # 2 + 4 + 6 + 8
    forwards = [c[1] for c in pen.calls if c[0] == "forward"]
    assert forwards == [2, 4, 6, 8]


def test_orbit_positions_lie_on_circle():
    frames = orbit_positions(8, 100)
    assert frames[0] == (100.0, 0.0)
    assert frames[2] == (0.0, 100.0)
    assert all(math.isclose(math.hypot(x, y), 100, abs_tol=0.02) for x, y in frames)


def test_animate_orbit_runs_one_frame_per_tick():
    pen, scheduled, redraws = FakePen(), [], []
    animate_orbit(pen, [(1, 1), (2, 2), (3, 3)], lambda fn, ms: scheduled.append((fn, ms)), lambda: redraws.append(1))
    while scheduled:
        fn, _ms = scheduled.pop(0)
        fn()
    assert [c for c in pen.calls if c[0] == "goto"] == [("goto", 1, 1), ("goto", 2, 2), ("goto", 3, 3)]
    assert pen.calls[0] == ("penup",) and len(redraws) == 3


def test_move_to_lifts_the_pen():
    pen = FakePen()
    move_to(pen, 5, -5)
    assert pen.calls == [("penup",), ("goto", 5, -5), ("pendown",)]
