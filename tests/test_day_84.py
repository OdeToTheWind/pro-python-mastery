"""Tests for Day 84 – Data Pipeline / ETL."""

import json
import logging

import pytest

from src.day_84_data_pipeline_etl.main import (
    Reading,
    RunStats,
    discover,
    extract,
    load,
    main,
    run_pipeline,
    seed_inbox,
    summarise,
    transform,
)


@pytest.fixture
def inbox(tmp_path):
    seed_inbox(tmp_path / "inbox")
    return tmp_path / "inbox"


def test_discover_filters_and_sorts(inbox):
    (inbox / ".hidden.csv").write_text("x", encoding="utf-8")
    assert [p.name for p in discover(inbox)] == ["legacy.csv", "north.csv", "south.jsonl"]


def test_extract_is_lazy_and_survives_bad_files(inbox):
    stats = RunStats()
    stream = extract(discover(inbox), stats)
    assert stats.files == 0  # nothing read yet
    records = list(stream)
    assert stats.files == 3 and stats.bad_files == ["legacy.csv"]
    assert len(records) == 7 and stats.rejected["invalid json"] == 1


@pytest.mark.parametrize(
    ("raw", "reason"),
    [({"station": "", "timestamp": "2026-10-01T08:00:00", "pm25": 1, "no2": 1}, "missing station"),
     ({"station": "a", "timestamp": "soon", "pm25": 1, "no2": 1}, "unrecognised timestamp"),
     ({"station": "a", "timestamp": "2026-10-01T08:00:00", "pm25": 5000, "no2": 1}, "pm25 out of range"),
     ({"station": "a", "timestamp": "2026-10-01T08:00:00", "pm25": "n/a", "no2": 1}, "could not convert"),
     ({"station": "a", "timestamp": "2026-10-01T08:00:00", "no2": 1}, "pm25 out of range")],
)
def test_transform_rejects_with_reason(raw, reason):
    stats = RunStats()
    assert list(transform([("f", raw)], stats)) == []
    assert reason in stats.quarantine[0]["reason"]


def test_transform_normalises_and_dedupes():
    stats = RunStats()
    rows = [("f", {"station": " south ", "timestamp": "01/10/2026 08:00", "pm25": "3", "no2": "4"})] * 2
    assert list(transform(rows, stats)) == [Reading("SOUTH", "2026-10-01T08:00", 3.0, 4.0)]
    assert stats.rejected["duplicate reading"] == 1


def test_load_is_atomic_and_counts(tmp_path):
    stats = RunStats()
    out = tmp_path / "o" / "r.jsonl"
    load([Reading("A", "t", 1.0, 2.0)], out, stats)
    assert stats.loaded == 1 and not out.with_suffix(".tmp").exists()
    assert summarise(out) == {"A": {"readings": 1, "avg_pm25": 1.0, "max_pm25": 1.0}}


def test_full_run(inbox, tmp_path, caplog):
    with caplog.at_level(logging.INFO, logger="airq.etl"):
        stats = run_pipeline(inbox, tmp_path / "out")
    summary = json.loads((tmp_path / "out" / "summary.json").read_text())
    assert summary["stats"]["loaded"] == stats.loaded == 3
    assert summary["stations"] == {"NORTH": {"readings": 2, "avg_pm25": 13.8, "max_pm25": 15.0},
                                   "SOUTH": {"readings": 1, "avg_pm25": 30.1, "max_pm25": 30.1}}
    quarantine = (tmp_path / "out" / "quarantine.jsonl").read_text().splitlines()
    assert len(quarantine) == sum(stats.rejected.values()) == 5
    assert any("skipping unreadable file legacy.csv" in r.message for r in caplog.records)


def test_empty_inbox(tmp_path):
    (tmp_path / "in").mkdir()
    stats = run_pipeline(tmp_path / "in", tmp_path / "out")
    assert stats.loaded == 0 and json.loads((tmp_path / "out" / "summary.json").read_text())["stations"] == {}


def test_main(capsys):
    main()
    assert '"NORTH"' in capsys.readouterr().out
