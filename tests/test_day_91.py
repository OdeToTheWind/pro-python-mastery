"""Tests for Day 91 – Type-safe Configuration System."""

from pathlib import Path
from typing import Literal

import pytest

from src.day_91_type_safe_configuration.main import (
    Channel,
    ConfigError,
    Database,
    Secret,
    Settings,
    coerce,
    describe,
    known_keys,
    load_settings,
    main,
    safe_dict,
)


def test_defaults_without_environment():
    settings = load_settings({"UNRELATED": "x"})
    assert settings == Settings() and settings.rollout.channel is Channel.STABLE


@pytest.mark.parametrize(
    ("raw", "hint", "expected"),
    [("42", int, 42), ("0.5", float, 0.5), ("YES", bool, True), ("off", bool, False),
     ("/data/fw", Path, Path("/data/fw")), ("Beta", Channel, Channel.BETA),
     ("a, b,,c", tuple[str, ...], ("a", "b", "c")), ("1,2", tuple[int, ...], (1, 2)),
     ("none", str | None, None), ("https://x", str | None, "https://x"), ("prod", Literal["dev", "prod"], "prod")],
)
def test_coerce_from_hints(raw, hint, expected):
    assert coerce(raw, hint) == expected


@pytest.mark.parametrize(
    ("raw", "hint", "message"),
    [("maybe", bool, "true/false"), ("x", int, "invalid literal"), ("qa", Literal["dev", "prod"], "dev, prod"),
     ("nightly", Channel, "stable, beta, canary")],
)
def test_coerce_errors(raw, hint, message):
    with pytest.raises(ValueError, match=message):
        coerce(raw, hint)
    with pytest.raises(TypeError, match="unsupported"):
        coerce("1", dict)


def test_nested_env_and_dotenv_precedence(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text("FLEET_DB__HOST=db.internal\nFLEET_WORKERS=8\nFLEET_WEBHOOK_URL\n", encoding="utf-8")
    settings = load_settings({"FLEET_WORKERS": "16", "FLEET_ROLLOUT__REGIONS": "eu,us"}, env_file)
    assert settings.db.host == "db.internal" and settings.workers == 16  # real env beats .env
    assert settings.rollout.regions == ("eu", "us") and settings.webhook_url is None


def test_all_problems_reported_at_once_without_leaking_secrets():
    with pytest.raises(ConfigError) as info:
        load_settings({"FLEET_WORKERS": "0", "FLEET_DB__PORT": "abc", "FLEET_ROLLOUT__BATCH_PERCENT": "150",
                       "FLEET_DB_HOST": "typo"})
    problems = info.value.problems
    assert problems[0] == "unknown setting FLEET_DB_HOST (typo?)"
    assert any(p.startswith("FLEET_DB__PORT='abc'") for p in problems)
    assert "rollout.batch_percent must be in (0, 100]" in problems and "workers must be 1–64" in problems


def test_prod_rules():
    with pytest.raises(ConfigError) as info:
        load_settings({"FLEET_ENVIRONMENT": "prod", "FLEET_ROLLOUT__CHANNEL": "canary"})
    assert info.value.problems == ["prod may not roll out the canary channel", "db.password is required in prod"]
    ok = load_settings({"FLEET_ENVIRONMENT": "prod", "FLEET_DB__PASSWORD": "pw"})
    assert ok.db.password.reveal() == "pw"


def test_secret_never_printed():
    db = Database(password=Secret("hunter2"))
    assert "hunter2" not in repr(db) and "hunter2" not in f"{db.password}"
    assert Secret("a") == Secret("a") and Secret("a") != "a" and len({Secret("a"), Secret("a")}) == 1
    dumped = safe_dict(Settings(db=db))
    assert dumped["db"]["password"] == "**********" and dumped["rollout"]["regions"] == ["eu"]
    assert dumped["firmware_dir"] == "firmware" and safe_dict(Settings())["db"]["password"] == ""


def test_settings_are_frozen():
    with pytest.raises(AttributeError):
        Settings().workers = 9  # type: ignore[misc]


def test_describe_and_known_keys_cover_every_field():
    rows = describe()
    assert len(rows) - 2 == len(known_keys()) == 13
    assert "| `FLEET_ROLLOUT__REGIONS` | comma-separated str | `eu` |" in rows
    assert "| `FLEET_ROLLOUT__CHANNEL` | stable / beta / canary | `stable` |" in rows
    assert "| `FLEET_WEBHOOK_URL` | str (optional) | `None` |" in rows
    assert "| `FLEET_ENVIRONMENT` | dev / staging / prod | `dev` |" in rows


def test_main(capsys):
    main()
    out = capsys.readouterr().out
    assert "s3cr3t" not in out and "unknown setting FLEET_DB_PASSWORD" in out and "'apac'" in out
