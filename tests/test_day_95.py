"""Tests for Day 95 – Performance-critical Module."""

import math

import pytest

from src.day_95_performance_critical_module.main import (
    benchmark,
    haversine,
    main,
    nearest_grid,
    nearest_naive,
    nearest_numba,
    nearest_numpy,
    profile_hotspots,
    random_city,
)

FAST = [nearest_grid, nearest_numpy, nearest_numba]


def test_haversine_known_distances():
    assert haversine((0, 0), (0, 0)) == 0
    assert haversine((0, 0), (0, 1)) == pytest.approx(111.19, abs=0.01)  # one degree on the equator
    assert haversine((38.7223, -9.1393), (40.4168, -3.7038)) == pytest.approx(502.7, abs=1)  # Lisbon–Madrid


@pytest.mark.parametrize("impl", FAST)
@pytest.mark.parametrize("seed", [1, 2, 3])
def test_fast_paths_match_baseline(impl, seed):
    riders, drivers = random_city(60, seed), random_city(150, seed + 100)
    assert impl(riders, drivers) == nearest_naive(riders, drivers)


@pytest.mark.parametrize("impl", FAST)
def test_sparse_and_far_away_drivers(impl):
    riders = [(38.70, -9.10), (60.0, 10.0), (-33.9, 151.2)]
    drivers = [(38.71, -9.11), (59.9, 10.7), (40.4, -3.7)]
    assert impl(riders, drivers) == nearest_naive(riders, drivers) == [0, 1, 1]  # Sydney is closer to Oslo than to Madrid


@pytest.mark.parametrize("impl", FAST)
def test_no_drivers(impl):
    with pytest.raises(ValueError, match="no drivers"):
        impl([(0.0, 0.0)], [])


def test_numpy_batches_and_empty_riders():
    riders, drivers = random_city(37, 5), random_city(20, 6)
    assert nearest_numpy(riders, drivers, batch=8) == nearest_numpy(riders, drivers)
    assert nearest_numpy([], drivers) == [] and nearest_grid([], drivers) == []


def test_profile_finds_the_hotspot():
    riders, drivers = random_city(5, 1), random_city(50, 2)
    names = [name for name, _calls in profile_hotspots(lambda: nearest_naive(riders, drivers), top=3)]
    assert "haversine" in names
    counts = dict(profile_hotspots(lambda: nearest_naive(riders, drivers), top=10))
    assert counts["haversine"] == 5 * 50


def test_benchmark_checks_correctness_then_times():
    timings = benchmark(random_city(40, 1), random_city(200, 2), repeat=1)
    assert set(timings) == {"naive", "grid", "numpy", "numba"} and all(t > 0 for t in timings.values())
    assert timings["numpy"] < timings["naive"]


def test_grid_cell_size_does_not_change_answer():
    riders, drivers = random_city(30, 7), random_city(90, 8)
    expected = nearest_naive(riders, drivers)
    assert all(nearest_grid(riders, drivers, cell_deg=c) == expected for c in (0.005, 0.05, 1.0))
    assert not math.isnan(haversine(riders[0], drivers[0]))


def test_main(capsys):
    main()
    out = capsys.readouterr().out
    assert "faster than naive" in out and "numba available:" in out
