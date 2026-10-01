"""Day 87 – Capstone: Plugin-style Architecture.

Scenario: a *team chat-bot* whose commands (``!roll``, ``!weather``,
``!standup`` …) come from plugins. Built-in commands register with a
decorator, local plugins are loaded from a folder at runtime, and installed
packages contribute commands through ``importlib.metadata`` entry points – a
broken or incompatible plugin is reported, never fatal.

Deliverables (syllabus):
* Decorator-based registration (``@registry.command(...)`` with aliases)
* Dynamic loading (``importlib.util.spec_from_file_location``)
* Entry points (``importlib.metadata.entry_points(group=...)``)
* Plugin contract: API version check, isolation of failures, conflicts
"""

from __future__ import annotations

import importlib.metadata
import importlib.util
import logging
import random
import shlex
import sys
from collections.abc import Callable, Iterable
from dataclasses import dataclass, field
from pathlib import Path
from types import ModuleType

DELIVERABLES: dict[str, str] = {
    "decorator registration": "CommandRegistry.command",
    "load plugins from a folder": "load_plugin_dir",
    "load plugins from entry points": "load_entry_points",
    "plugin API version contract": "PluginError",
    "message dispatch": "Bot.handle",
    "built-in plugin": "builtin_plugin",
}

API_VERSION = 1
ENTRY_POINT_GROUP = "chatbot.plugins"
log = logging.getLogger("chatbot")
Handler = Callable[..., str]


class PluginError(Exception):
    """Raised for a plugin that cannot be used (bad API version, name clash, import error)."""


@dataclass
class Command:
    name: str
    func: Handler
    help: str
    plugin: str
    aliases: tuple[str, ...] = ()


@dataclass
class CommandRegistry:
    commands: dict[str, Command] = field(default_factory=dict)
    current_plugin: str = "core"

    def command(self, name: str, *, aliases: Iterable[str] = (), help: str = "") -> Callable[[Handler], Handler]:
        """Decorator: registers the function and returns it unchanged (still unit-testable)."""

        def decorator(func: Handler) -> Handler:
            cmd = Command(name, func, help or (func.__doc__ or "").strip(), self.current_plugin, tuple(aliases))
            for key in (name, *cmd.aliases):
                if key in self.commands:
                    raise PluginError(f"{self.current_plugin}: command {key!r} already provided by "
                                      f"{self.commands[key].plugin}")
            for key in (name, *cmd.aliases):
                self.commands[key] = cmd
            return func

        return decorator

    def install(self, plugin_name: str, setup: Callable[[CommandRegistry], object], api: int) -> None:
        if api != API_VERSION:
            raise PluginError(f"{plugin_name}: needs plugin API {api}, bot provides {API_VERSION}")
        before = dict(self.commands)
        self.current_plugin = plugin_name
        try:
            setup(self)
        except Exception:
            self.commands = before  # all-or-nothing: a half-registered plugin is worse than none
            raise
        finally:
            self.current_plugin = "core"

    def unique(self) -> list[Command]:
        return sorted({id(c): c for c in self.commands.values()}.values(), key=lambda c: c.name)


def builtin_plugin(registry: CommandRegistry) -> None:
    @registry.command("help", aliases=["?"])
    def help_(*_args: str) -> str:
        """List commands."""
        return ", ".join(f"!{c.name}" for c in registry.unique())

    @registry.command("roll", aliases=["dice"])
    def roll(sides: str = "6", *, rng: random.Random | None = None) -> str:
        """Roll a die: !roll 20"""
        n = int(sides)
        if not 2 <= n <= 1000:
            raise ValueError("sides must be 2–1000")
        return f"🎲 {(rng or random.Random()).randint(1, n)}"


def _module_from_file(path: Path) -> ModuleType:
    name = f"chatbot_plugin_{path.stem}"
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise PluginError(f"{path.name}: not importable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    try:
        spec.loader.exec_module(module)
    except Exception as exc:
        del sys.modules[name]
        raise PluginError(f"{path.name}: import failed: {exc!r}") from exc
    return module


def _install_module(registry: CommandRegistry, name: str, module: ModuleType) -> None:
    setup = getattr(module, "setup", None)
    if not callable(setup):
        raise PluginError(f"{name}: missing setup(registry)")
    registry.install(name, setup, getattr(module, "API_VERSION", 0))


def load_plugin_dir(registry: CommandRegistry, folder: Path) -> list[str]:
    """Load every ``*.py`` in ``folder`` (not ``_private.py``); return the errors."""
    errors = []
    for path in sorted(folder.glob("*.py")):
        if path.name.startswith("_"):
            continue
        try:
            _install_module(registry, path.stem, _module_from_file(path))
            log.info("loaded plugin %s", path.stem)
        except Exception as exc:
            errors.append(str(exc) if isinstance(exc, PluginError) else f"{path.stem}: {exc!r}")
    return errors


def load_entry_points(registry: CommandRegistry,
                      discover: Callable[..., Iterable[importlib.metadata.EntryPoint]] = importlib.metadata.entry_points,
                      ) -> list[str]:
    """Installed packages declare ``[project.entry-points."chatbot.plugins"] name = "pkg.mod:setup"``."""
    errors = []
    for ep in discover(group=ENTRY_POINT_GROUP):
        try:
            setup = ep.load()
            registry.install(ep.name, setup, getattr(setup, "api_version", API_VERSION))
        except Exception as exc:
            errors.append(str(exc) if isinstance(exc, PluginError) else f"{ep.name}: {exc!r}")
    return errors


class Bot:
    def __init__(self, registry: CommandRegistry) -> None:
        self.registry = registry

    def handle(self, message: str) -> str | None:
        if not message.startswith("!"):
            return None  # ordinary chat, not for the bot
        try:
            name, *args = shlex.split(message[1:])
        except ValueError as exc:
            return f"⚠️ {exc}"
        cmd = self.registry.commands.get(name.lower())
        if cmd is None:
            return f"unknown command !{name} – try !help"
        try:
            return cmd.func(*args)
        except TypeError:
            return f"usage: !{cmd.name} – {cmd.help}"
        except Exception as exc:
            log.exception("plugin %s crashed", cmd.plugin)
            return f"⚠️ !{cmd.name} failed: {exc}"


DEMO_PLUGINS = {
    "weather.py": (
        "API_VERSION = 1\n"
        "FORECAST = {'berlin': 'cloudy 14°C', 'lisbon': 'sunny 24°C'}\n"
        "def setup(registry):\n"
        "    @registry.command('weather', aliases=['w'])\n"
        "    def weather(*city):\n"
        "        '''Forecast: !weather Lisbon'''\n"
        "        name = ' '.join(city).lower()\n"
        "        return FORECAST.get(name, f'no forecast for {name}')\n"),
    "standup.py": (
        "API_VERSION = 1\n"
        "def setup(registry):\n"
        "    @registry.command('standup')\n"
        "    def standup(person):\n"
        "        '''Post an update: !standup <name>'''\n"
        "        return f'{person}: yesterday / today / blockers?'\n"),
    "legacy.py": "API_VERSION = 0\ndef setup(registry):\n    pass\n",
    "broken.py": "import does_not_exist\n",
}


def write_demo_plugins(folder: Path) -> None:
    folder.mkdir(parents=True, exist_ok=True)
    for name, code in DEMO_PLUGINS.items():
        (folder / name).write_text(code, encoding="utf-8")


def main() -> None:
    import tempfile

    print("Day 87 – Chat-bot plugins\n")
    registry = CommandRegistry()
    registry.install("builtin", builtin_plugin, API_VERSION)
    with tempfile.TemporaryDirectory() as tmp:
        write_demo_plugins(Path(tmp))
        for error in load_plugin_dir(registry, Path(tmp)) + load_entry_points(registry):
            print("plugin skipped:", error)
    bot = Bot(registry)
    for message in ("!help", "!w lisbon", "!standup Ada", "!standup", "!roll 1", "!dance", "hi all"):
        print(f"{message!r:>16} -> {bot.handle(message)}")


if __name__ == "__main__":
    main()
