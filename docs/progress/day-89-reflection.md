# Day 89 – Background Task Runner Reflection

**Date:** 2026-10-01 · **Level:** Capstone · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_89_background_task_runner/main.py`](../../src/day_89_background_task_runner/main.py) · **Tests:** [`tests/test_day_89.py`](../../tests/test_day_89.py) (11 tests)

## Scenario
A *home-lab backup scheduler*. A small daemon reads job specs such as ``"every 15 minutes"`` or ``"daily at 02:30"``, runs each job as a child process with a timeout, never runs two copies of the same job at once, refuses to start twice (PID file) and shuts down gracefully on SIGTERM.

## Syllabus deliverables
> Scheduling with schedule or APScheduler and process management

| Deliverable | Implemented in |
|---|---|
| ✅ parse schedule specs | `parse_spec` |
| ✅ register jobs with schedule | `TaskRunner.add` |
| ✅ run child processes with timeouts | `run_command` |
| ✅ stop long-running workers | `stop_process` |
| ✅ single-instance PID file | `pid_file` |
| ✅ graceful shutdown on signals | `TaskRunner.install_signal_handlers` |
| ✅ main loop | `TaskRunner.run` |

## Key learnings
- The `schedule` library expresses jobs in readable specs; a tick loop with `Event.wait` stays responsive.
- `subprocess.run(timeout=...)` without `shell=True` runs jobs safely; terminate → wait → kill stops stubborn ones.
- An `O_EXCL` PID file prevents two runners, and stale locks from crashed runs are recovered.

## Pitfalls I hit (and how I fixed them)
- Without overlap protection, a slow job piles up more and more copies of itself.

## Run it
```bash
python -m src.day_89_background_task_runner.main
pytest tests/test_day_89.py -v
```

## Next step
- Process files larger than memory on Day 90.
