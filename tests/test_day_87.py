"""Tests for Day 87 – Plugin-style Architecture."""

import random
from importlib.metadata import EntryPoint

import pytest

from src.day_87_plugin_architecture.main import (
    API_VERSION,
    ENTRY_POINT_GROUP,
    Bot,
    CommandRegistry,
    PluginError,
    builtin_plugin,
    load_entry_points,
    load_plugin_dir,
    main,
    write_demo_plugins,
)


@pytest.fixture
def registry():
    reg = CommandRegistry()
    reg.install("builtin", builtin_plugin, API_VERSION)
    return reg


def test_decorator_registers_and_returns_function(registry):
    @registry.command("echo", aliases=["e"])
    def echo(*words):
        """Repeat text."""
        return " ".join(words)

    assert echo("hi") == "hi"
    assert registry.commands["e"] is registry.commands["echo"] and registry.commands["echo"].help == "Repeat text."
    roll = registry.commands["dice"].func
    assert roll("20", rng=random.Random(1)) == f"🎲 {random.Random(1).randint(1, 20)}"


def test_name_clash_is_rejected_and_rolled_back(registry):
    def clashing(reg):
        @reg.command("fresh")
        def fresh():
            return ""

        @reg.command("other", aliases=["dice"])
        def other():
            return ""

    with pytest.raises(PluginError, match="'dice' already provided by builtin"):
        registry.install("games", clashing, API_VERSION)
    assert "fresh" not in registry.commands


def test_api_version_mismatch():
    with pytest.raises(PluginError, match="needs plugin API 2"):
        CommandRegistry().install("future", lambda r: None, 2)


def test_folder_loading_isolates_bad_plugins(registry, tmp_path):
    write_demo_plugins(tmp_path)
    (tmp_path / "_helpers.py").write_text("raise SystemExit('never imported')", encoding="utf-8")
    (tmp_path / "nosetup.py").write_text("X = 1\n", encoding="utf-8")
    (tmp_path / "crashy.py").write_text("API_VERSION = 1\ndef setup(r):\n    raise RuntimeError('db down')\n",
                                        encoding="utf-8")
    errors = load_plugin_dir(registry, tmp_path)
    assert {e.split(":")[0] for e in errors} == {"broken.py", "legacy", "nosetup", "crashy"}
    assert "ModuleNotFoundError" in next(e for e in errors if e.startswith("broken"))
    assert {"weather", "w", "standup"} <= set(registry.commands)
    assert registry.commands["standup"].plugin == "standup"


def test_entry_points_are_discovered(registry):
    good = EntryPoint("games", "src.day_87_plugin_architecture.main:builtin_plugin", ENTRY_POINT_GROUP)
    missing = EntryPoint("ghost", "no_such_pkg.plugin:setup", ENTRY_POINT_GROUP)
    seen = {}

    def fake_discover(group):
        seen["group"] = group
        return [good, missing]

    errors = load_entry_points(registry, fake_discover)
    assert seen["group"] == "chatbot.plugins"
    assert errors[0].startswith("games: command 'help' already provided")  # same commands twice
    assert errors[1].startswith("ghost: ModuleNotFoundError")
    assert load_entry_points(CommandRegistry(), lambda group: [good]) == []


@pytest.mark.parametrize(
    ("message", "reply"),
    [("hello", None),
     ("!w berlin", "cloudy 14°C"),
     ('!weather "rio de janeiro"', "no forecast for rio de janeiro"),
     ("!standup", "usage: !standup – Post an update: !standup <name>"),
     ("!roll 1", "⚠️ !roll failed: sides must be 2–1000"),
     ("!ROLL x", "⚠️ !roll failed: invalid literal for int() with base 10: 'x'"),
     ("!nope", "unknown command !nope – try !help"),
     ('!weather "unclosed', "⚠️ No closing quotation")],
)
def test_bot_dispatch(registry, tmp_path, message, reply):
    write_demo_plugins(tmp_path)
    load_plugin_dir(registry, tmp_path)
    assert Bot(registry).handle(message) == reply


def test_help_lists_unique_commands(registry):
    assert Bot(registry).handle("!?") == "!help, !roll"


def test_main(capsys):
    main()
    out = capsys.readouterr().out
    assert "plugin skipped: legacy: needs plugin API 0" in out and "sunny 24°C" in out
