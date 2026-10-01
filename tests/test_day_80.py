"""Tests for Day 80 – Profiling & Performance.

Performance assertions use large, structural gaps (O(n²) vs O(n)) so they stay
reliable on slow CI machines.
"""

import pytest

from src.day_80_profiling_performance.main import (
    compare_timings,
    main,
    make_orders,
    memory_profile,
    order_totals,
    peak_allocation_kib,
    profile_hotspots,
    render_csv_fast,
    render_csv_slow,
    report_fast,
    report_slow,
    tax_rate,
)

ORDERS = make_orders(3000)


def test_fast_version_gives_identical_results():
    assert report_fast(ORDERS) == report_slow(ORDERS)
    assert render_csv_fast(ORDERS) == render_csv_slow(ORDERS)
    assert report_fast([]) == report_slow([]) == {"customers": 0, "repeat_orders": 0, "gross_cents": 0}


def test_report_numbers():
    result = report_fast(make_orders(10))
    assert result["customers"] + result["repeat_orders"] == 10


def test_cprofile_finds_the_hotspots():
    hot = profile_hotspots(lambda: report_slow(ORDERS))
    names = [name for name, _calls, _t in hot]
    assert names[0] == "report_slow"
    assert ("slow_tax_rate", 3000) in [(n, c) for n, c, _t in hot]


def test_cache_removes_repeated_work():
    tax_rate.cache_clear()
    list(order_totals(ORDERS))
    info = tax_rate.cache_info()
    assert info.misses == 5 and info.hits == len(ORDERS) - 5


def test_timeit_shows_large_speedup():
    timings = compare_timings({"slow": lambda: report_slow(ORDERS), "fast": lambda: report_fast(ORDERS)},
                              number=1, repeat=2)
    assert timings["fast"] * 5 < timings["slow"]


def test_generator_allocates_less_than_list():
    as_list = peak_allocation_kib(lambda: sum([o.amount_cents * 1.2 for o in ORDERS]))
    as_gen = peak_allocation_kib(lambda: sum(order_totals(ORDERS)))
    assert as_gen * 5 < as_list


def test_memory_profiler_samples_process_memory():
    pytest.importorskip("memory_profiler")
    result = memory_profile(lambda: [bytes(1024) for _ in range(5000)])
    assert result["samples"] >= 1 and result["peak_mib"] > 0


def test_main(capsys):
    main()
    out = capsys.readouterr().out
    assert "same answer:" in out and "× faster" in out
