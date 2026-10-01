"""Day 37 – Python Turtle.

Scenario: a *greeting-card artist* – draws shapes, a star burst, a spiral and
an animated orbit with ``turtle``.

The drawing functions accept any object with turtle-like methods (a
``Protocol``), so the geometry is unit-tested with a recording fake pen and the
real window is only opened by ``main()``.

Deliverables (syllabus):
* Graphics with Turtle (screen, pen, colours)
* Shapes (regular polygons, stars)
* Drawing logic (angles, loops, spirals)
* Animations (``tracer``/``update`` + ``ontimer`` frame loop)
"""

from __future__ import annotations

import contextlib
import math
from collections.abc import Callable
from typing import Protocol

DELIVERABLES: dict[str, str] = {
    "graphics setup": "main",
    "shapes: regular polygons": "draw_polygon",
    "shapes: stars": "draw_star",
    "drawing logic: angles": "exterior_angle",
    "drawing logic: spiral": "draw_spiral",
    "animation frames": "orbit_positions",
    "animation loop with ontimer": "animate_orbit",
}


class Pen(Protocol):
    def forward(self, distance: float) -> object: ...
    def right(self, angle: float) -> object: ...
    def penup(self) -> object: ...
    def pendown(self) -> object: ...
    def goto(self, x: float, y: float) -> object: ...


def move_to(pen: Pen, x: float, y: float) -> None:
    """Jump to (x, y) without drawing a line."""
    pen.penup()
    pen.goto(x, y)
    pen.pendown()


def exterior_angle(sides: int) -> float:
    """Turning angle for a regular polygon: the turns must add up to 360°."""
    if sides < 3:
        raise ValueError("a polygon needs at least three sides")
    return 360 / sides


def star_angle(points: int) -> float:
    """Turning angle for a single-stroke star (5 points → 144°)."""
    if points < 5 or points % 2 == 0:
        raise ValueError("single-stroke stars need an odd number of points ≥ 5")
    return 180 - 180 / points


def draw_polygon(pen: Pen, sides: int, length: float) -> float:
    """Draw a regular polygon and return the total angle turned (always 360)."""
    angle = exterior_angle(sides)
    for _ in range(sides):
        pen.forward(length)
        pen.right(angle)
    return angle * sides


def draw_star(pen: Pen, points: int, size: float) -> None:
    angle = star_angle(points)
    for _ in range(points):
        pen.forward(size)
        pen.right(angle)


def draw_spiral(pen: Pen, steps: int, growth: float = 4, turn: float = 59) -> float:
    """Each segment is longer than the last – returns the total distance drawn."""
    total = 0.0
    for step in range(1, steps + 1):
        pen.forward(step * growth)
        pen.right(turn)
        total += step * growth
    return total


def orbit_positions(frames: int, radius: float) -> list[tuple[float, float]]:
    """Pre-compute animation frames: points on a circle."""
    return [
        (round(radius * math.cos(2 * math.pi * f / frames), 2),
         round(radius * math.sin(2 * math.pi * f / frames), 2))
        for f in range(frames)
    ]


def animate_orbit(
    pen: Pen,
    frames: list[tuple[float, float]],
    schedule: Callable[[Callable[[], None], int], object],
    redraw: Callable[[], object],
    delay_ms: int = 40,
) -> None:
    """Move the pen to one frame per tick. ``schedule`` is ``screen.ontimer``."""
    remaining = list(frames)

    def tick() -> None:
        if not remaining:
            return
        x, y = remaining.pop(0)
        pen.goto(x, y)
        redraw()
        schedule(tick, delay_ms)

    pen.penup()
    tick()


def main() -> None:  # pragma: no cover – opens a window
    try:
        import turtle
    except ImportError:
        print("Turtle needs Tkinter. Install python3-tk (Linux) or the full Python installer.")
        return
    try:
        screen = turtle.Screen()
    except turtle.Terminator:
        return
    except Exception as exc:  # TclError when no display is available
        print(f"Cannot open a window here: {exc}")
        return
    try:
        screen.title("Day 37 – Greeting card")
        screen.bgcolor("midnight blue")
        pen = turtle.Turtle()
        pen.speed(0)
        pen.color("gold")
        draw_star(pen, 5, 150)
        move_to(pen, -200, -150)
        pen.color("light sky blue")
        draw_polygon(pen, 6, 60)
        move_to(pen, 180, -120)
        pen.color("plum")
        draw_spiral(pen, 30, growth=3)
        moon = turtle.Turtle(shape="circle")
        moon.color("white")
        screen.tracer(0)
        animate_orbit(moon, orbit_positions(120, 220), screen.ontimer, screen.update)
        screen.exitonclick()
    finally:
        with contextlib.suppress(turtle.Terminator):
            turtle.bye()


if __name__ == "__main__":
    main()
