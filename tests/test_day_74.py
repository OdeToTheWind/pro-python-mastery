"""Tests for Day 74 – Multiprocessing (small tiles keep the suite fast)."""

import pytest

from src.day_74_concurrency_multiprocessing.main import (
    Workload,
    analyse_tiles,
    analyse_tiles_pool,
    benchmark,
    bright_pixels,
    bright_pixels_shared,
    choose_executor,
    count_with_shared_value,
    make_tile,
)

TILES = [make_tile(seed, size=20_000) for seed in range(1, 5)]
EXPECTED = [bright_pixels(t) for t in TILES]


def test_make_tile_is_deterministic():
    assert make_tile(3, 100) == make_tile(3, 100) != make_tile(4, 100)
    assert 0 < bright_pixels(TILES[0]) < len(TILES[0])


def test_process_pool_executor_matches_sequential():
    assert analyse_tiles(TILES, workers=2) == EXPECTED


def test_pool_map_matches_sequential():
    assert analyse_tiles_pool(TILES, workers=2) == EXPECTED


def test_shared_memory_slices_add_up():
    assert bright_pixels_shared(TILES[0], parts=3) == EXPECTED[0]


def test_shared_memory_is_released(monkeypatch):
    from multiprocessing import shared_memory

    created = []
    original = shared_memory.SharedMemory

    def tracking(*args, **kwargs):
        block = original(*args, **kwargs)
        if kwargs.get("create"):
            created.append(block.name)
        return block

    monkeypatch.setattr(shared_memory, "SharedMemory", tracking)
    bright_pixels_shared(TILES[1], parts=2)
    with pytest.raises(FileNotFoundError):
        original(name=created[0])  # unlinked → no longer attachable


def test_shared_value_with_lock():
    assert count_with_shared_value(TILES) == sum(EXPECTED)


@pytest.mark.parametrize(
    ("work", "starts_with"),
    [(Workload(False, 1, 1), "threads"), (Workload(True, 0.001, 1), "single process"),
     (Workload(True, 2, 500), "processes + shared memory"), (Workload(True, 2, 5), "process pool")],
)
def test_choose_executor(work, starts_with):
    assert choose_executor(work).startswith(starts_with)


def test_benchmark_verifies_results():
    report = benchmark(TILES, lambda tiles: analyse_tiles(tiles, workers=2))
    assert set(report) == {"sequential_s", "parallel_s", "speedup", "cpus"}
    with pytest.raises(AssertionError):
        benchmark(TILES, lambda tiles: [0] * len(tiles))
