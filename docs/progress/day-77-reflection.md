# Day 77 – Logging & Configuration Reflection

**Date:** 2026-10-01 · **Level:** Advanced · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_77_logging_configuration/main.py`](../../src/day_77_logging_configuration/main.py) · **Tests:** [`tests/test_day_77.py`](../../tests/test_day_77.py) (9 tests)

## Scenario
A *food-delivery dispatch service* that reads its settings from INI, YAML or TOML files (plus environment overrides) and logs to the console for humans and to a rotating JSON file for machines.

## Syllabus deliverables
> Logging handlers, formatters, levels, configparser, YAML, and TOML

| Deliverable | Implemented in |
|---|---|
| ✅ configparser (INI) | `load_ini` |
| ✅ YAML (safe\_load) | `load_yaml` |
| ✅ TOML (tomllib) | `load_toml` |
| ✅ layered settings with env overrides | `load_settings` |
| ✅ logging levels | `Settings.log_level` |
| ✅ JSON formatter | `JsonFormatter` |
| ✅ handlers + dictConfig | `configure_logging` |
| ✅ rotating file handler | `configure_logging` |
| ✅ contextual logging (extra fields) | `dispatch` |

## Key learnings
- Handlers decide *where* logs go, formatters *how* they look, levels *what* gets through – per logger and per handler.
- `dictConfig` keeps logging configuration declarative and in one place.
- Settings should be layered (defaults < file < environment), type-converted and validated once at start-up.

## Pitfalls I hit (and how I fixed them)
- `yaml.load` can construct arbitrary Python objects – always use `yaml.safe_load` for configuration.

## Run it
```bash
python -m src.day_77_logging_configuration.main
pytest tests/test_day_77.py -v
```

## Next step
- Test the configuration loader thoroughly with pytest on Day 78.
