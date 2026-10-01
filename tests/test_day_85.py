"""Tests for Day 85 – Concurrent File / Network Processor (local aiohttp server)."""

import asyncio
import hashlib
import threading
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

import pytest

from src.day_85_concurrent_file_network_processor.main import (
    EPISODES,
    Progress,
    checksum_files,
    choose_executor,
    compress_files,
    download_all,
    main,
    mirror,
    with_feed_server,
)


def fetch(tmp_path, names, **server):
    limit = server.pop("limit", 3)
    retries = server.pop("retries", 2)
    timeout = server.pop("timeout", 2.0)

    async def work(url):
        return await download_all(url, names, tmp_path, limit=limit, retries=retries, timeout=timeout)

    return asyncio.run(with_feed_server(work, **server))


def test_downloads_respect_the_semaphore_limit(tmp_path):
    results, peak = fetch(tmp_path, list(EPISODES), limit=2, delay=0.02)
    assert all(r.ok for r in results) and peak == 2
    assert (tmp_path / "ep03.mp3").read_bytes() == EPISODES["ep03.mp3"]


def test_downloads_overlap_in_time(tmp_path):
    start = time.perf_counter()
    fetch(tmp_path, list(EPISODES), limit=5, delay=0.1)
    assert time.perf_counter() - start < 0.4  # five 0.1 s requests run together


def test_retry_after_503_and_404_is_not_retried(tmp_path):
    results, _ = fetch(tmp_path, ["ep01.mp3", "nope.mp3"], flaky={"ep01.mp3"})
    assert results[0].ok and results[1].detail == "HTTP 404"


def test_gives_up_and_leaves_no_partial_file(tmp_path):
    results, _ = fetch(tmp_path, ["ep01.mp3"], flaky={"ep01.mp3"}, retries=0)
    assert not results[0].ok and "HTTP 503" in results[0].detail
    assert list(tmp_path.iterdir()) == []


def test_timeout_is_reported(tmp_path):
    results, _ = fetch(tmp_path, ["ep01.mp3"], delay=0.5, timeout=0.1, retries=0)
    assert results[0].detail.endswith("TimeoutError")


def test_checksums_in_threads_with_progress(tmp_path):
    files = []
    for i in range(6):
        path = tmp_path / f"f{i}.bin"
        path.write_bytes(bytes([i]) * 1000)
        files.append(path)
    progress = Progress(len(files) + 1)
    hashes, errors = checksum_files([*files, tmp_path / "gone.bin"], workers=3, progress=progress)
    assert hashes["f2.bin"] == hashlib.sha256(bytes([2]) * 1000).hexdigest()
    assert len(errors) == 1 and errors[0].startswith("gone.bin") and progress.percent == 100.0


def test_progress_lock_is_exact_under_contention():
    progress = Progress(8000)
    threads = [threading.Thread(target=lambda: [progress.tick() for _ in range(1000)]) for _ in range(8)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert progress.done == 8000 and Progress(0).percent == 100.0


def test_compression_in_processes(tmp_path):
    (tmp_path / "rep.txt").write_bytes(b"a" * 10_000)
    (tmp_path / "empty.txt").write_bytes(b"")
    ratios = compress_files([tmp_path / "rep.txt", tmp_path / "empty.txt"], workers=2)
    assert ratios["rep.txt"] < 0.01 and ratios["empty.txt"] == 1.0


def test_choose_executor():
    with choose_executor("io") as pool:
        assert isinstance(pool, ThreadPoolExecutor)
    with choose_executor("cpu", workers=1) as pool:
        assert isinstance(pool, ProcessPoolExecutor)
    with pytest.raises(ValueError, match="io"):
        choose_executor("gpu")


def test_mirror_end_to_end(tmp_path):
    from aiohttp.test_utils import TestServer

    from src.day_85_concurrent_file_network_processor.main import make_feed_app

    async def start():
        server = TestServer(make_feed_app())
        await server.start_server()
        return server

    loop = asyncio.new_event_loop()
    server = loop.run_until_complete(start())
    thread = threading.Thread(target=loop.run_forever, daemon=True)
    thread.start()
    try:
        report = mirror(str(server.make_url("")).rstrip("/"), ["ep01.mp3", "x.mp3"], tmp_path)
    finally:
        asyncio.run_coroutine_threadsafe(server.close(), loop).result()
        loop.call_soon_threadsafe(loop.stop)
        thread.join()
        loop.close()
    assert list(report.hashes) == ["ep01.mp3"] and report.failures == ["x.mp3: HTTP 404"]
    assert report.compressed["ep01.mp3"] < 0.1


def test_main(capsys):
    main()
    out = capsys.readouterr().out
    assert "ERR missing.mp3" in out and "peak 3 in flight" in out
