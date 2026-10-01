"""Tests for Day 72 – Advanced Typing."""

from typing import get_args, get_type_hints

import pytest

from src.day_72_advanced_typing.main import (
    BAD_SNIPPET,
    AcmeBot,
    Command,
    HasBattery,
    Repository,
    RobotixDrone,
    RobotPayload,
    closest,
    from_payload,
    low_battery,
    main,
    parse_command,
    scale,
    type_check,
)


def test_protocol_accepts_unrelated_classes():
    acme, drone = AcmeBot("a"), RobotixDrone("d")
    assert acme.move("E", 2) == (2, 0)
    assert drone.move("E", 2) == (4, 0)
    assert not issubclass(RobotixDrone, AcmeBot)
    assert closest([acme, drone], (3, 0)) is acme


def test_closest_preserves_type_and_validates():
    bots = [AcmeBot("a", 5, 5), AcmeBot("b", 1, 1)]
    assert closest(bots, (0, 0)).id == "b"
    with pytest.raises(ValueError):
        closest([], (0, 0))


def test_battery_drains_and_runtime_checkable_protocol():
    bot = AcmeBot("a", battery=3)
    bot.move("N", 5)
    assert bot.battery == 0
    assert isinstance(bot, HasBattery) and not isinstance(RobotixDrone("d"), HasBattery)
    assert low_battery([bot, RobotixDrone("d"), AcmeBot("ok")]) == ["a"]


def test_generic_repository():
    repo: Repository[AcmeBot] = Repository()
    repo.add(AcmeBot("a"))
    assert repo.get("a").id == "a" and repo.get("zz") is None and len(repo) == 1
    with pytest.raises(KeyError):
        repo.add(AcmeBot("a"))


def test_constrained_typevar():
    assert scale(3, 4) == 12 and scale(1.5, 2.0) == 3.0


def test_literal_narrowing():
    assert set(get_args(Command)) == {"move", "charge", "pick", "drop"}
    assert parse_command("charge") == "charge"
    with pytest.raises(ValueError):
        parse_command("dance")


def test_typed_dict_is_plain_dict_with_declared_keys():
    assert RobotPayload.__required_keys__ == {"id", "vendor", "x", "y", "battery"}
    assert RobotPayload.__optional_keys__ == {"firmware"}
    bot = from_payload({"id": "a9", "vendor": "acme", "x": 2, "y": 3, "battery": 50})
    assert bot.position == (2, 3)
    assert "battery" in get_type_hints(RobotPayload)


def test_mypy_rejects_the_bad_snippet():
    ok, report = type_check(BAD_SNIPPET)
    assert not ok
    assert 'Argument 1 to "add" of "Repository" has incompatible type "RobotixDrone"' in report
    assert "Literal['UP']" in report  # invalid Direction literal


def test_mypy_accepts_correct_code():
    ok, report = type_check(
        "from src.day_72_advanced_typing.main import AcmeBot, Repository\n"
        "repo: Repository[AcmeBot] = Repository()\nrepo.add(AcmeBot('x'))\n"
    )
    assert ok, report


def test_pyright_optional():
    ok, report = type_check("x: int = 1\n", checker="pyright")
    assert ok or "error" in report


def test_main(capsys):
    main()
    assert "mypy accepts the bad snippet? False" in capsys.readouterr().out
