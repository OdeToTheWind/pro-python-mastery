"""Tests for Day 65 – Generators & yield."""

import inspect
import itertools

from src.day_65_generators_yield.main import (
    container_sizes,
    kwh_total,
    main,
    meter_readings,
    peak_detector,
    peak_memory_kib,
    single_use_demo,
    traced_readings,
)


def test_meter_readings_is_a_generator_function():
    assert inspect.isgeneratorfunction(meter_readings)
    assert list(itertools.islice(meter_readings(), 4)) == [500, 1537, 796, 1609]  # (v * 7 + 37) % 2000


def test_infinite_generator_is_safe_with_islice():
    assert len(list(itertools.islice(meter_readings(), 10_000))) == 10_000


def test_lazy_evaluation_is_observable():
    log = []
    stream = traced_readings([1, 2], log)
    assert log == []  # the body has not started yet
    assert next(stream) == 1
    assert log == ["generator created – no work yet", "produced 1"]
    assert list(stream) == [2]
    assert log[-1] == "exhausted"


def test_kwh_total():
    assert kwh_total([1000] * 60) == 1.0  # 1 kW for 60 minutes
    assert kwh_total([]) == 0


def test_peak_detector_keeps_state_between_yields():
    assert list(peak_detector([100, 950, 900, 1900, 0], threshold=800)) == [(1, 950), (3, 1900)]
    assert list(peak_detector([], 1)) == []


def test_generator_is_much_smaller_than_list():
    sizes = container_sizes(100_000)
    assert sizes["generator"] < 500 < sizes["list"]


def test_tracemalloc_shows_memory_benefit():
    n = 100_000
    as_list = peak_memory_kib(lambda: sum([i for i in range(n)]))
    as_gen = peak_memory_kib(lambda: sum(i for i in range(n)))
    assert as_gen * 10 < as_list


def test_generators_are_single_use():
    assert single_use_demo() == (30, 0)


def test_main(capsys):
    main()
    assert "after creating the generator: []" in capsys.readouterr().out
