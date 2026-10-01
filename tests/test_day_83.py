"""Tests for Day 83 – Robust CLI Application."""

import json
from datetime import date

import pytest

from src.day_83_robust_cli_application.main import (
    EXIT_CODES,
    __version__,
    build_parser,
    load_config,
    main,
    run,
    streak,
)

TODAY = date(2026, 10, 1)


@pytest.fixture
def env(tmp_path):
    return {"HABITS_DATA_FILE": str(tmp_path / "habits.json")}


def cli(capsys, env, *argv):
    code = run(list(argv), env=env, today=TODAY)
    captured = capsys.readouterr()
    return code, captured.out.strip(), captured.err.strip()


def test_full_workflow_and_json_output(capsys, env):
    assert cli(capsys, env, "add", "  Read  Books ")[0] == 0
    cli(capsys, env, "done", "read books", "--on", "2026-09-29")
    cli(capsys, env, "done", "read books", "--on", "yesterday")
    code, out, _ = cli(capsys, env, "done", "read books")
    assert code == 0 and json.loads(cli(capsys, env, "--format", "json", "list")[1]) == {"read books": 3}
    assert "streak" in out


def test_streak_logic():
    assert streak(["2026-09-29", "2026-09-30"], TODAY) == 2  # today not done yet still counts
    assert streak(["2026-09-28", "2026-10-01"], TODAY) == 1
    assert streak([], TODAY) == 0


@pytest.mark.parametrize(
    ("argv", "code", "message"),
    [(["streak", "yoga"], EXIT_CODES["not_found"], "no habit called 'yoga'"),
     (["done", "yoga", "--on", "2030-01-01"], EXIT_CODES["not_found"], "no habit"),
     (["add", "x" * 41], EXIT_CODES["usage"], "1–40 characters"),
     (["done", "yoga", "--on", "someday"], EXIT_CODES["usage"], "invalid date"),
     (["fly"], EXIT_CODES["usage"], "invalid choice")],
)
def test_error_exit_codes(capsys, env, argv, code, message):
    result, _out, err = cli(capsys, env, *argv)
    assert result == code and message in err


def test_future_dates_rejected(capsys, env):
    cli(capsys, env, "add", "yoga")
    code, _out, err = cli(capsys, env, "done", "yoga", "--on", "2026-12-24")
    assert code == EXIT_CODES["usage"] and "future" in err


def test_duplicate_add(capsys, env):
    cli(capsys, env, "add", "yoga")
    assert cli(capsys, env, "add", "YOGA")[0] == EXIT_CODES["error"]


def test_version_and_help(capsys, env):
    assert run(["--version"], env=env) == 0
    assert __version__ in capsys.readouterr().out
    assert run(["--help"], env=env) == 0
    assert "add" in capsys.readouterr().out


def test_verbose_and_quiet_are_exclusive(capsys, env):
    assert run(["-v", "-q", "list"], env=env) == EXIT_CODES["usage"]


def test_logging_goes_to_stderr_with_verbosity(capsys, env):
    code, out, err = cli(capsys, env, "-vv", "add", "walk")
    assert code == 0 and "walk" in out and "INFO" not in out
    assert "INFO: added walk" in err and "DEBUG: saved 1 habits" in err


def test_config_layers(tmp_path, env):
    cfg = tmp_path / "habits.toml"
    cfg.write_text('[habits]\ndata_file = "/tmp/from-file.json"\ndefault_format = "json"\n', encoding="utf-8")
    assert str(load_config(cfg, env={}).data_file) == "/tmp/from-file.json"
    config = load_config(cfg, env=env)
    assert config.data_file.name == "habits.json" and config.default_format == "json"  # env wins


def test_invalid_config_and_corrupt_data(capsys, tmp_path, env):
    bad = tmp_path / "bad.toml"
    bad.write_text('[habits]\ndefault_format = "xml"\n', encoding="utf-8")
    assert cli(capsys, env, "--config", str(bad), "list")[0] == EXIT_CODES["usage"]
    (tmp_path / "habits.json").write_text("{oops", encoding="utf-8")
    code, _, err = cli(capsys, env, "list")
    assert code == EXIT_CODES["error"] and "corrupt" in err


def test_config_command(capsys, env):
    code, out, _ = cli(capsys, env, "config", "--path-only")
    assert code == 0 and out.endswith("habits.json")


def test_parser_structure():
    parser = build_parser()
    assert parser.prog == "habits"
    assert parser.parse_args(["done", "x", "--on", "2026-01-01"]).on == date(2026, 1, 1)


def test_main(capsys):
    main()
    assert "(exit code 3)" in capsys.readouterr().out
