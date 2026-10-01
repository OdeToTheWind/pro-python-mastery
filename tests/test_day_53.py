"""Tests for Day 53 – Local Persistence.

Every test uses ``tmp_path``: nothing in the working tree (or the user's real
progress file) is ever read, overwritten or deleted.
"""

import json

import pytest

from src.day_53_local_persistence import main as day53
from src.day_53_local_persistence.main import (
    DEFAULTS,
    ProgressStore,
    default_store_path,
    main,
    migrate,
)


@pytest.fixture
def path(tmp_path):
    return tmp_path / "progress.json"


def test_fresh_store_uses_defaults_without_writing(path):
    store = ProgressStore(path)
    assert store.data == DEFAULTS
    assert not path.exists()


def test_save_and_load_round_trip(path):
    store = ProgressStore(path)
    store.add_xp(50)
    store.update(language="fr", settings={"sound": False})
    reloaded = ProgressStore(path).data
    assert reloaded["xp"] == 50 and reloaded["language"] == "fr"
    assert reloaded["settings"] == {"sound": False, "daily_goal": 20}  # nested defaults merged


def test_update_rejects_unknown_fields(path):
    with pytest.raises(KeyError):
        ProgressStore(path).update(coins=10)


def test_add_xp_validation(path):
    with pytest.raises(ValueError):
        ProgressStore(path).add_xp(0)


def test_migrate_v1():
    assert migrate({"version": 1, "score": 7, "level": 2}) == {"version": 2, "xp": 7}
    assert migrate({"score": 3}) == {"version": 2, "xp": 3}
    assert migrate({"version": 2, "xp": 1}) == {"version": 2, "xp": 1}


def test_corrupt_file_is_backed_up_not_lost(path):
    path.write_text("{broken", encoding="utf-8")
    store = ProgressStore(path)
    assert store.data == DEFAULTS
    assert path.with_suffix(".json.corrupt").read_text(encoding="utf-8") == "{broken"


def test_non_object_json_is_treated_as_corrupt(path):
    path.write_text("[1, 2]", encoding="utf-8")
    assert ProgressStore(path).data == DEFAULTS


def test_atomic_save_preserves_old_file_on_failure(path, monkeypatch):
    store = ProgressStore(path)
    store.add_xp(10)

    def failing_replace(_a, _b):
        raise OSError("disk full")

    monkeypatch.setattr(day53.os, "replace", failing_replace)
    with pytest.raises(OSError):
        store.add_xp(5)
    assert json.loads(path.read_text(encoding="utf-8"))["xp"] == 10
    assert sorted(p.name for p in path.parent.iterdir()) == ["progress.json"]


def test_default_location_is_git_ignored():
    assert default_store_path().parent.name == ".data"


def test_main(capsys, path):
    main(path)
    out = capsys.readouterr().out
    assert "'xp': 150" in out and "backup kept: True" in out
