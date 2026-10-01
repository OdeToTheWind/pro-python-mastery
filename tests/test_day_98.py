"""Tests for Day 98 – Scientific / Simulation Mini-project."""

import math

import numpy as np
import pytest

from src.day_98_scientific_simulation.main import (
    SIRParams,
    chain_binomial,
    final_size,
    herd_immunity_threshold,
    main,
    simulate_rk4,
    summarise_runs,
    sweep_numpy,
)


def test_params_validation_and_r0():
    assert SIRParams(0.3, 0.1).r0 == pytest.approx(3.0)
    assert SIRParams(0.3, 0.1, population=100, infected=10, vaccinated=0.5).initial() == (40.0, 10.0, 50.0)
    for bad in ({"beta": -1, "gamma": 0.1}, {"beta": 1, "gamma": 0}, {"beta": 1, "gamma": 1, "vaccinated": 1},
                {"beta": 1, "gamma": 1, "infected": 0}):
        with pytest.raises(ValueError):
            SIRParams(**bad)


def test_rk4_conserves_population_and_matches_final_size():
    p = SIRParams(0.3, 0.1)
    days = simulate_rk4(p, days=300)
    assert all(math.isclose(sum(day), p.population, rel_tol=1e-9) for day in days)
    assert days[-1][2] / p.population == pytest.approx(final_size(3.0), abs=0.002)


def test_below_threshold_no_epidemic():
    days = simulate_rk4(SIRParams(0.08, 0.1), days=200)
    assert max(d[1] for d in days) == pytest.approx(10.0)  # never grows
    assert final_size(0.8) == 0.0 and herd_immunity_threshold(0.8) == 0.0


def test_vaccination_above_threshold_stops_growth():
    p = SIRParams(0.3, 0.1, vaccinated=0.7)  # threshold for R0=3 is 66.7 %
    days = simulate_rk4(p, days=100)
    assert max(d[1] for d in days) == pytest.approx(10.0) and herd_immunity_threshold(3) == pytest.approx(2 / 3)


@pytest.mark.parametrize(("r0", "z"), [(1.5, 0.5828), (2.0, 0.7968), (3.0, 0.9405)])
def test_final_size_known_values(r0, z):
    value = final_size(r0)
    assert value == pytest.approx(z, abs=1e-4) and value == pytest.approx(1 - math.exp(-r0 * value))


def test_numpy_sweep_matches_pure_python():
    betas = np.array([0.15, 0.3])
    sweep = sweep_numpy(betas, gamma=0.1, days=150, steps_per_day=10)
    for k, beta in enumerate(betas):
        days = simulate_rk4(SIRParams(float(beta), 0.1), days=150, steps_per_day=10)
        peak_day = max(range(len(days)), key=lambda d: days[d][1])
        assert sweep["peak"][k] == pytest.approx(days[peak_day][1], rel=1e-9)
        assert sweep["peak_day"][k] == peak_day
    assert sweep["peak"][1] > sweep["peak"][0] and list(sweep["r0"]) == pytest.approx([1.5, 3.0])


def test_monte_carlo_is_seeded_and_matches_branching_theory():
    p = SIRParams(beta=0.2, gamma=0.1, population=5_000, infected=1)
    a, b = chain_binomial(p, runs=1500, seed=7), chain_binomial(p, runs=1500, seed=7)
    assert np.array_equal(a, b) and a.min() >= 1 and a.max() <= p.population
    summary = summarise_runs(a, p.population)
    low, high = summary["p_major_ci"]
    # for a single case, P(major outbreak) ≈ 1 − 1/R0 = 0.5 (discrete-time recovery shifts it a little)
    assert 0.35 < summary["p_major"] < 0.6 and low < summary["p_major"] < high
    assert summary["mean_major_share"] == pytest.approx(final_size(2.0), abs=0.05)


def test_summary_without_major_outbreaks():
    summary = summarise_runs(np.array([1, 2, 3]), 1000)
    assert summary["p_major"] == 0.0 and summary["major_share_95"] == (0.0, 0.0)
    no_spread = chain_binomial(SIRParams(beta=0.0, gamma=0.5, population=100, infected=2), runs=10)
    assert set(no_spread.tolist()) == {2}


def test_main(capsys):
    main()
    out = capsys.readouterr().out
    assert "R0 = 3.0" in out and "herd-immunity threshold: 67%" in out and "p_major" in out
