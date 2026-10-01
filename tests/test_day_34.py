"""Tests for Day 34 – Optional, Required and Default Parameters."""

import pytest

from src.day_34_optional_required_default_parameters.main import (
    add_label,
    describe_parameters,
    main,
    ordering_rules_demo,
    schedule_job,
    with_defaults,
)


def test_minimal_call_uses_defaults():
    job = schedule_job("build", notify="a@b.c")
    assert (job.priority, job.tags, job.retries, job.env) == (5, (), 3, {})


def test_args_and_kwargs_are_collected():
    job = schedule_job("t", 7, "x", "y", notify="a@b.c", retries=0, CI="1", OS="linux")
    assert job.tags == ("x", "y")
    assert job.env == {"CI": "1", "OS": "linux"}


def test_required_keyword_only_parameter():
    with pytest.raises(TypeError, match="notify"):
        schedule_job("build")  # type: ignore[call-arg]


def test_positional_only_parameters():
    with pytest.raises(TypeError):
        schedule_job(name="build", notify="a@b.c")  # type: ignore[call-arg]


@pytest.mark.parametrize(
    "kwargs", [{"notify": "nobody"}, {"notify": "a@b.c", "retries": -1}],
)
def test_validation(kwargs):
    with pytest.raises(ValueError):
        schedule_job("x", **kwargs)


def test_priority_range():
    with pytest.raises(ValueError):
        schedule_job("x", 11, notify="a@b.c")


def test_describe_parameters():
    assert describe_parameters(schedule_job) == [
        ("name", "POSITIONAL_ONLY", True),
        ("priority", "POSITIONAL_ONLY", False),
        ("tags", "VAR_POSITIONAL", False),
        ("retries", "KEYWORD_ONLY", False),
        ("notify", "KEYWORD_ONLY", True),
        ("env", "VAR_KEYWORD", False),
    ]


def test_ordering_rules():
    results = ordering_rules_demo()
    assert results["legal full signature"] == "ok"
    assert all(v.startswith("SyntaxError") for k, v in results.items() if k != "legal full signature")


def test_none_sentinel_gives_fresh_list():
    assert add_label("a") == ["a"]
    assert add_label("b") == ["b"]
    shared = ["x"]
    assert add_label("y", shared) is shared and shared == ["x", "y"]


def test_with_defaults_forwards_and_allows_override():
    team = with_defaults(schedule_job, notify="team@x.io", retries=1)
    assert team("lint").notify == "team@x.io"
    assert team("lint", 2, "fast", retries=5).retries == 5


def test_main(capsys):
    main()
    assert "notify    KEYWORD_ONLY           required" in capsys.readouterr().out
