"""Tests for Day 77 – Logging & Configuration."""

import json
import logging

import pytest

from src.day_77_logging_configuration.main import (
    SAMPLE_CONFIGS,
    JsonFormatter,
    Settings,
    configure_logging,
    dispatch,
    load_ini,
    load_settings,
    load_toml,
    load_yaml,
    main,
)


@pytest.fixture
def configs(tmp_path):
    for name, text in SAMPLE_CONFIGS.items():
        (tmp_path / name).write_text(text, encoding="utf-8")
    return tmp_path


def test_parsers():
    assert load_ini(SAMPLE_CONFIGS["dispatch.ini"]) == {"max_drivers": "40", "log_level": "warning"}
    assert load_ini("[other]\nx = 1\n") == {}
    assert load_yaml(SAMPLE_CONFIGS["dispatch.yaml"]) == {"max_drivers": 60, "surge_multiplier": 1.5}
    assert load_toml(SAMPLE_CONFIGS["dispatch.toml"]) == {"service": "dispatch-eu", "max_drivers": 70}


def test_yaml_safe_load_refuses_python_objects():
    with pytest.raises(Exception, match="could not determine a constructor"):
        load_yaml("dispatch: !!python/object/apply:os.system ['echo hacked']")
    with pytest.raises(ValueError):
        load_yaml("- just\n- a list\n")


@pytest.mark.parametrize(("name", "max_drivers"), [("dispatch.ini", 40), ("dispatch.yaml", 60), ("dispatch.toml", 70)])
def test_each_format_loads_into_typed_settings(configs, name, max_drivers):
    settings = load_settings(configs / name, env={})
    assert settings.max_drivers == max_drivers and isinstance(settings.max_drivers, int)


def test_layering_env_overrides_file(configs):
    settings = load_settings(configs / "dispatch.ini", env={"DISPATCH_MAX_DRIVERS": "99", "OTHER": "x"})
    assert settings.max_drivers == 99 and settings.log_level == "WARNING"
    assert load_settings(None, env={}) == Settings()


@pytest.mark.parametrize(
    ("env", "error"),
    [({"DISPATCH_LOG_LEVEL": "loud"}, ValueError), ({"DISPATCH_MAX_DRIVERS": "0"}, ValueError),
     ({"DISPATCH_SURGE_MULTIPLIER": "9"}, ValueError), ({"DISPATCH_COLOUR": "red"}, KeyError)],
)
def test_invalid_settings_rejected(env, error):
    with pytest.raises(error):
        load_settings(None, env=env)


def test_unsupported_format(tmp_path):
    path = tmp_path / "c.json"
    path.write_text("{}", encoding="utf-8")
    with pytest.raises(ValueError, match="unsupported"):
        load_settings(path, env={})


def test_json_formatter_includes_context_and_exception():
    record = logging.LogRecord("svc", logging.ERROR, __file__, 1, "boom %s", ("now",), None)
    record.order_id = "A-9"
    data = json.loads(JsonFormatter().format(record))
    assert data["message"] == "boom now" and data["order_id"] == "A-9" and data["level"] == "ERROR"
    try:
        _ = 1 / 0
    except ZeroDivisionError:
        import sys

        record.exc_info = sys.exc_info()
    assert "ZeroDivisionError" in json.loads(JsonFormatter().format(record))["exception"]


def test_logging_levels_and_handlers(tmp_path, capsys):
    settings = Settings(service="dispatch-test", log_level="WARNING", log_file=str(tmp_path / "logs" / "d.log"))
    logger = configure_logging(settings)
    assert dispatch(logger, "A-1", 30, settings) == "dispatched"
    assert dispatch(logger, "A-2", 2, settings) == "dispatched"
    assert dispatch(logger, "A-3", 0, settings) == "queued"
    for handler in logger.handlers:
        handler.flush()
    console = capsys.readouterr().err
    assert "order dispatched" not in console  # INFO filtered on the console
    assert "low driver availability: 2 free" in console and "no drivers available" in console
    lines = [json.loads(line) for line in (tmp_path / "logs" / "d.log").read_text().splitlines()]
    assert [line["level"] for line in lines].count("DEBUG") == 2  # file keeps everything
    assert lines[-1] == {**lines[-1], "level": "ERROR", "order_id": "A-3"}
    assert any(line.get("driver") == "D030" for line in lines)
    for handler in logger.handlers:
        handler.close()


def test_main(capsys):
    main()
    out = capsys.readouterr().out
    assert "dispatch.yaml  →" in out and '"order_id": "A-3"' in out
