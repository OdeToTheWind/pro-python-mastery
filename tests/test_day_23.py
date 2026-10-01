"""Tests for Day 23 – Scope and Local/Global Variables."""

import pytest

from src.day_23_scope_local_global_variables import main as day23


@pytest.fixture(autouse=True)
def _restore_environment():
    original = day23.ENVIRONMENT
    yield
    day23.set_environment(original)


def test_legb_trace():
    assert day23.legb_trace() == {
        "inside local()": "local",
        "inside no_local()": "enclosing",
        "module level": "global",
        "len is built-in": "builtins",
    }


def test_global_keyword_rebinds_module_variable():
    assert day23.set_environment("staging") == "production"
    assert day23.ENVIRONMENT == "staging"
    assert day23.current_environment() == "staging"


def test_unbound_local_error():
    assert day23.unbound_local_demo() == "UnboundLocalError"


def test_rate_limiter_nonlocal_state_is_per_closure():
    a, b = day23.make_rate_limiter(2), day23.make_rate_limiter(1)
    assert [a(), a(), a()] == [True, True, False]
    assert [b(), b()] == [True, False]


def test_closure_cells_expose_captured_values():
    limiter = day23.make_rate_limiter(3)
    limiter()
    assert day23.closure_cells(limiter) == {"calls": 1, "max_calls": 3}


def test_feature_flags_hold_their_own_state():
    first, second = day23.FeatureFlags(), day23.FeatureFlags()
    first.enable("beta")
    assert first.is_enabled("beta") and not second.is_enabled("beta")


def test_main_restores_environment(capsys):
    day23.main()
    assert "production → staging" in capsys.readouterr().out
    assert day23.ENVIRONMENT == "production"
