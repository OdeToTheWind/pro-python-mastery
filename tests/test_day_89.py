"""Tests for Day 89 – Background Task Runner."""

import os
import signal
import subprocess
import sys
import threading
import time

import pytest
import schedule

from src.day_89_background_task_runner.main import (
    TaskRunner,
    main,
    parse_spec,
    pid_file,
    run_command,
    stop_process,
)

PY = sys.executable


@pytest.mark.parametrize(
    ("spec", "unit", "interval", "at"),
    [("every 15 minutes", "minutes", 15, None),
     ("every hour", "hours", 1, None),
     ("Every 2 days at 03:15", "days", 2, "03:15:00"),
     ("daily at 02:30", "days", 1, "02:30:00")],
)
def test_parse_spec(spec, unit, interval, at):
    job = parse_spec(spec, schedule.Scheduler())
    assert (job.unit, job.interval, str(job.at_time) if job.at_time else None) == (unit, interval, at)


@pytest.mark.parametrize("spec", ["sometimes", "every 5 minutes at 10:00", "every fortnight"])
def test_parse_spec_rejects(spec):
    with pytest.raises(ValueError):
        parse_spec(spec, schedule.Scheduler())


def test_run_command_outcomes():
    assert run_command("ok", [PY, "-c", "print('hi')"], 5).output == "hi"
    failed = run_command("fail", [PY, "-c", "import sys; sys.exit('disk full')"], 5)
    assert failed.returncode == 1 and failed.output == "disk full" and not failed.ok
    slow = run_command("slow", [PY, "-c", "import time; time.sleep(3)"], 0.2)
    assert slow.timed_out and slow.seconds < 2
    assert run_command("missing", ["definitely-not-a-binary-xyz"], 1).returncode == 127


def test_stop_process_escalates_to_kill():
    stubborn = subprocess.Popen([PY, "-c", "import signal, time; signal.signal(signal.SIGTERM, signal.SIG_IGN);"
                                 "print('ready', flush=True); time.sleep(30)"], stdout=subprocess.PIPE, text=True)
    stubborn.stdout.readline()
    assert stop_process(stubborn, grace=0.2) == -signal.SIGKILL
    stubborn.stdout.close()
    polite = subprocess.Popen([PY, "-c", "import time; time.sleep(30)"], text=True)
    assert stop_process(polite) == -signal.SIGTERM
    assert stop_process(polite) == -signal.SIGTERM  # already stopped: just returns


def test_pid_file_single_instance_and_stale_lock(tmp_path):
    path = tmp_path / "run" / "runner.pid"
    with pid_file(path) as pid:
        assert path.read_text() == str(pid) == str(os.getpid())
        with pytest.raises(RuntimeError, match="already running"), pid_file(path):
            pass
    assert not path.exists()
    dead = subprocess.Popen([PY, "-c", "pass"])
    dead.wait()
    path.write_text(str(dead.pid))
    with pid_file(path):  # stale pid → lock recovered
        assert path.read_text() == str(os.getpid())


def test_runner_executes_jobs_and_records_history():
    runner = TaskRunner()
    runner.add("echo", "every 1 second", [PY, "-c", "print('backup')"])
    runner.scheduler.run_all()
    assert [(r.name, r.output, r.ok) for r in runner.history] == [("echo", "backup", True)]
    assert runner.scheduler.get_jobs("echo")


def test_overlapping_runs_are_skipped():
    runner = TaskRunner()
    runner.add("long", "every 1 second", [PY, "-c", "import time; time.sleep(0.5)"], background=True)
    runner.scheduler.run_all()
    runner.scheduler.run_all()  # first run still busy
    deadline = time.monotonic() + 5
    while runner.running and time.monotonic() < deadline:
        time.sleep(0.05)
    assert runner.skipped == ["long"] and len(runner.history) == 1


def test_loop_stops_on_signal():
    runner = TaskRunner()
    restore = runner.install_signal_handlers()
    try:
        threading.Timer(0.1, lambda: os.kill(os.getpid(), signal.SIGTERM)).start()
        start = time.monotonic()
        runner.run(tick=0.02)
        assert runner.stop_event.is_set() and time.monotonic() - start < 2
    finally:
        restore()
    assert signal.getsignal(signal.SIGTERM) == signal.SIG_DFL
    assert TaskRunner().run(tick=0, max_ticks=3) == 3


def test_main(capsys):
    main()
    out = capsys.readouterr().out
    assert "'snapshot ok'" in out and "timeout" in out and "Every 1 day at 02:30:00" in out
