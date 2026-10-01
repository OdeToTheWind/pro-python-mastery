"""Tests for Day 73 – Threading."""

import time

from src.day_73_concurrency_threading.main import (
    Heartbeat,
    ViewCounter,
    cpu_work,
    fetch_thumbnails,
    gil_experiment,
    hammer,
    main,
    upload_pipeline,
)


def test_thread_pool_runs_io_concurrently_and_keeps_order():
    results, seconds = fetch_thumbnails(list(range(10)), workers=10, latency=0.05)
    assert results == [f"thumb-{i}.jpg" for i in range(10)]
    assert seconds < 0.5 * 10 * 0.05  # far faster than 10 sequential waits


def test_lock_prevents_lost_updates():
    counter = ViewCounter()
    hammer(counter.safe_increment, threads=8, per_thread=150)
    assert counter.views == 1200


def test_race_condition_loses_updates():
    counter = ViewCounter()
    hammer(counter.unsafe_increment, threads=8, per_thread=150)
    assert counter.views < 1200  # read-modify-write without a lock overwrites updates


def test_queue_pipeline_processes_everything():
    done, errors = upload_pipeline(["a.jpg", "b.png", "c.gif", "d.jpg"], consumers=2)
    assert done == ["A.JPG", "B.PNG", "D.JPG"]
    assert errors == ["unsupported file c.gif"]


def test_queue_pipeline_empty_input():
    assert upload_pipeline([], consumers=3) == ([], [])


def test_heartbeat_stops_cleanly():
    beat = Heartbeat(0.005)
    beat.start()
    time.sleep(0.05)
    beat.stop()
    assert not beat.is_alive() and beat.beats >= 1
    frozen = beat.beats
    time.sleep(0.02)
    assert beat.beats == frozen


def test_gil_experiment_shapes():
    result = gil_experiment(tasks=4, n=50_000, latency=0.03)
    assert result["io_speedup"] > 2  # I/O waits overlap
    if result["gil_enabled"]:
        assert result["cpu_speedup"] < 2.5  # pure-Python CPU work can't run in parallel under the GIL


def test_cpu_work_deterministic():
    assert cpu_work(10) == sum(i * i % 7 for i in range(10))


def test_main(capsys):
    main()
    out = capsys.readouterr().out
    assert "with Lock 1600" in out and "pipeline:" in out
