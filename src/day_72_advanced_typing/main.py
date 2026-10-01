"""Day 72 – Advanced Typing.

Scenario: a *warehouse-robot fleet manager*. Robots from different vendors
share no base class, yet the dispatcher accepts any of them because they
satisfy a ``Protocol``. Payloads from the vendors' JSON APIs are described with
``TypedDict``; commands are restricted with ``Literal``; a generic repository
works for robots, shelves or anything with an ``id``.

Deliverables (syllabus):
* ``Protocol`` (structural typing, ``runtime_checkable``)
* ``TypeVar`` (bounded and constrained) and ``Generic`` classes
* ``TypedDict`` (required / ``NotRequired`` keys) and ``Literal``
* Checking with mypy (run programmatically; pyright used when installed)

Note: this module deliberately does *not* use ``from __future__ import annotations``:
with postponed (string) annotations, ``NotRequired[...]`` inside a ``TypedDict`` is
not evaluated at class creation, so the key would wrongly be treated as required.
"""

import os
import shutil
import subprocess
import tempfile
from collections.abc import Iterator, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import (
    Final,
    Generic,
    Literal,
    NotRequired,
    Protocol,
    TypedDict,
    TypeVar,
    get_args,
    runtime_checkable,
)

DELIVERABLES: dict[str, str] = {
    "Protocol (structural typing)": "Movable",
    "runtime_checkable Protocol": "HasBattery",
    "TypeVar bound to a Protocol": "closest",
    "constrained TypeVar": "scale",
    "Generic class": "Repository",
    "TypedDict with NotRequired": "RobotPayload",
    "Literal types": "Command",
    "Final constants": "MAX_SPEED",
    "checking with mypy": "type_check",
    "checking with pyright (optional)": "type_check",
}

Command = Literal["move", "charge", "pick", "drop"]
Direction = Literal["N", "E", "S", "W"]
MAX_SPEED: Final = 2.5  # m/s – mypy rejects any reassignment


class Movable(Protocol):
    """Anything with a position and a ``move`` method – no inheritance required."""

    @property
    def position(self) -> tuple[int, int]: ...

    def move(self, direction: Direction, steps: int = 1) -> tuple[int, int]: ...


@runtime_checkable
class HasBattery(Protocol):
    battery: int


class Identified(Protocol):
    @property
    def id(self) -> str: ...


class RobotPayload(TypedDict):
    """Shape of the vendor JSON – checked statically, a plain dict at runtime."""

    id: str
    vendor: Literal["acme", "robotix"]
    x: int
    y: int
    battery: int
    firmware: NotRequired[str]


_DELTAS: dict[Direction, tuple[int, int]] = {"N": (0, 1), "E": (1, 0), "S": (0, -1), "W": (-1, 0)}


@dataclass
class AcmeBot:
    id: str
    x: int = 0
    y: int = 0
    battery: int = 100

    @property
    def position(self) -> tuple[int, int]:
        return self.x, self.y

    def move(self, direction: Direction, steps: int = 1) -> tuple[int, int]:
        dx, dy = _DELTAS[direction]
        self.x, self.y = self.x + dx * steps, self.y + dy * steps
        self.battery = max(0, self.battery - steps)
        return self.position


@dataclass
class RobotixDrone:
    """A different vendor's class – unrelated to AcmeBot, yet also ``Movable``."""

    id: str
    coords: list[int] = field(default_factory=lambda: [0, 0])

    @property
    def position(self) -> tuple[int, int]:
        return self.coords[0], self.coords[1]

    def move(self, direction: Direction, steps: int = 1) -> tuple[int, int]:
        dx, dy = _DELTAS[direction]
        self.coords = [self.coords[0] + 2 * dx * steps, self.coords[1] + 2 * dy * steps]  # flies 2× faster
        return self.position


# Classic TypeVar spelling (the syllabus topic). The PEP 695 equivalent would be
# ``def closest[M: Movable](...)`` and ``def scale[N: (int, float)](...)``.
M = TypeVar("M", bound=Movable)  # any type that satisfies Movable; return type stays precise
Number = TypeVar("Number", int, float)  # constrained: exactly int *or* float


def closest(robots: Sequence[M], target: tuple[int, int]) -> M:  # noqa: UP047 – teaching TypeVar
    """Returns the *same* concrete type it was given (AcmeBot in → AcmeBot out)."""
    if not robots:
        raise ValueError("no robots available")
    return min(robots, key=lambda r: abs(r.position[0] - target[0]) + abs(r.position[1] - target[1]))


def scale(value: Number, factor: Number) -> Number:  # noqa: UP047 – teaching TypeVar
    return value * factor


T = TypeVar("T", bound=Identified)


class Repository(Generic[T]):  # noqa: UP046 – teaching Generic
    """A generic in-memory store: ``Repository[AcmeBot]`` only accepts AcmeBots."""

    def __init__(self) -> None:
        self._items: dict[str, T] = {}

    def add(self, item: T) -> None:
        if item.id in self._items:
            raise KeyError(f"duplicate id {item.id!r}")
        self._items[item.id] = item

    def get(self, item_id: str) -> T | None:
        return self._items.get(item_id)

    def __iter__(self) -> Iterator[T]:
        return iter(self._items.values())

    def __len__(self) -> int:
        return len(self._items)


def parse_command(text: str) -> Command:
    """Narrow an untrusted string to the ``Command`` literal at runtime."""
    allowed: tuple[str, ...] = get_args(Command)
    if text not in allowed:
        raise ValueError(f"command must be one of {allowed}")
    return text  # type: ignore[return-value]


def from_payload(payload: RobotPayload) -> AcmeBot:
    return AcmeBot(payload["id"], payload["x"], payload["y"], payload["battery"])


def low_battery(robots: Sequence[object], threshold: int = 20) -> list[str]:
    """``runtime_checkable`` lets ``isinstance`` test for the protocol's attributes."""
    return [getattr(r, "id", "?") for r in robots if isinstance(r, HasBattery) and r.battery < threshold]


BAD_SNIPPET = '''
from src.day_72_advanced_typing.main import AcmeBot, Repository, RobotixDrone, parse_command
repo: Repository[AcmeBot] = Repository()
repo.add(RobotixDrone("d1"))          # wrong type for this repository
bot = AcmeBot("a1")
bot.move("UP")                        # not a valid Direction literal
'''


def type_check(source: str, checker: str = "mypy") -> tuple[bool, str]:
    """Type-check *source* with mypy (always) or pyright (if installed). Never executes it."""
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "snippet.py"
        path.write_text(source, encoding="utf-8")
        root = str(Path(__file__).resolve().parents[2])
        if checker == "mypy":
            from mypy import api

            previous = os.environ.get("MYPYPATH")
            os.environ["MYPYPATH"] = root  # lets mypy resolve `import src....`
            try:
                out, err, status = api.run([str(path), "--no-error-summary", "--hide-error-context",
                                            "--cache-dir", str(Path(tmp) / ".mypy")])
            finally:
                if previous is None:
                    os.environ.pop("MYPYPATH", None)
                else:
                    os.environ["MYPYPATH"] = previous
            return status == 0, out + err
        exe = shutil.which("pyright")
        if exe is None:
            return True, "pyright not installed – skipped"
        result = subprocess.run([exe, str(path)], capture_output=True, text=True, cwd=root, check=False)
        return result.returncode == 0, result.stdout


def main() -> None:
    print("Day 72 – Robot fleet typing\n")
    acme, drone = AcmeBot("a1", battery=15), RobotixDrone("d1")
    acme.move("N", 3)
    drone.move("E", 2)
    fleet: list[AcmeBot | RobotixDrone] = [acme, drone]
    print("closest to (4, 0):", closest(fleet, (4, 0)).id)
    repo: Repository[AcmeBot] = Repository()
    repo.add(acme)
    repo.add(from_payload({"id": "a2", "vendor": "acme", "x": 1, "y": 1, "battery": 90}))
    print("repo:", [bot.id for bot in repo], "| low battery:", low_battery([acme, drone]))
    print("scale int/float:", scale(3, 4), scale(1.5, 2.0), "| command:", parse_command("pick"))
    ok, report = type_check(BAD_SNIPPET)
    print("mypy accepts the bad snippet?", ok)
    print(report.strip())


if __name__ == "__main__":
    main()
