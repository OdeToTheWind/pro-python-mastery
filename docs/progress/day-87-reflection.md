# Day 87 – Plugin-style Architecture Reflection

**Date:** 2026-10-01 · **Level:** Capstone · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_87_plugin_architecture/main.py`](../../src/day_87_plugin_architecture/main.py) · **Tests:** [`tests/test_day_87.py`](../../tests/test_day_87.py) (8 tests)

## Scenario
A *team chat-bot* whose commands (``!roll``, ``!weather``, ``!standup`` …) come from plugins. Built-in commands register with a decorator, local plugins are loaded from a folder at runtime, and installed packages contribute commands through ``importlib.metadata`` entry points – a broken or incompatible plugin is reported, never fatal.

## Syllabus deliverables
> Entry points, dynamic loading, and decorator-based registration

| Deliverable | Implemented in |
|---|---|
| ✅ decorator registration | `CommandRegistry.command` |
| ✅ load plugins from a folder | `load_plugin_dir` |
| ✅ load plugins from entry points | `load_entry_points` |
| ✅ plugin API version contract | `PluginError` |
| ✅ message dispatch | `Bot.handle` |
| ✅ built-in plugin | `builtin_plugin` |

## Key learnings
- Decorator registration keeps plugins declarative: the function is registered and returned unchanged.
- `importlib.util.spec_from_file_location` loads plugin files at runtime; entry points discover installed ones.
- A plugin API version and all-or-nothing installation keep one broken plugin from breaking the bot.

## Pitfalls I hit (and how I fixed them)
- Silent name clashes let one plugin hijack another's command – detect and reject duplicates.

## Run it
```bash
./propython.sh 87                 # study mode: explanation, code map, notes and tests
python -m src.day_87_plugin_architecture.main
pytest tests/test_day_87.py -v
```

## Next step
- Generate reports in several formats on Day 88.
