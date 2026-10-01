"""Day 98 – Capstone: Scientific / Simulation Mini-project.

Scenario: an *epidemic outbreak simulator* for a city health department. A
deterministic SIR model is integrated in pure Python (RK4) and validated
against the analytical final-size equation; NumPy then sweeps hundreds of
transmission rates at once, and a stochastic chain-binomial Monte Carlo
answers the questions a planner actually asks: *how likely is a major
outbreak, and how large could it get?*

Deliverables (syllabus):
* A pure-Python simulation (SIR ODEs with a hand-written RK4 integrator)
* NumPy vectorisation (a parameter sweep integrated in one array program)
* Monte Carlo (seeded ``numpy.random.Generator``, thousands of runs)
* Scientific checks: conservation, analytical final size, confidence intervals
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any

import numpy as np

DELIVERABLES: dict[str, str] = {
    "model parameters and R0": "SIRParams",
    "pure-Python RK4 simulation": "simulate_rk4",
    "analytical final size (validation)": "final_size",
    "NumPy parameter sweep": "sweep_numpy",
    "stochastic Monte Carlo": "chain_binomial",
    "summary statistics with confidence intervals": "summarise_runs",
    "vaccination threshold": "herd_immunity_threshold",
}


@dataclass(frozen=True, slots=True)
class SIRParams:
    beta: float  # infections caused per infected person per day (in a fully susceptible city)
    gamma: float  # recovery rate per day (1 / infectious period)
    population: int = 100_000
    infected: int = 10
    vaccinated: float = 0.0  # share immune at the start

    def __post_init__(self) -> None:
        if self.beta < 0 or self.gamma <= 0 or not 0 <= self.vaccinated < 1:
            raise ValueError("need beta ≥ 0, gamma > 0 and 0 ≤ vaccinated < 1")
        if not 0 < self.infected <= self.population:
            raise ValueError("initial infected must be within the population")

    @property
    def r0(self) -> float:
        return self.beta / self.gamma

    def initial(self) -> tuple[float, float, float]:
        immune = self.vaccinated * self.population
        return self.population - self.infected - immune, float(self.infected), immune


def _derivatives(s: float, i: float, beta: float, gamma: float, n: float) -> tuple[float, float, float]:
    new_infections = beta * s * i / n
    recoveries = gamma * i
    return -new_infections, new_infections - recoveries, recoveries


def simulate_rk4(p: SIRParams, days: int = 365, steps_per_day: int = 10) -> list[tuple[float, float, float]]:
    """Classic 4th-order Runge–Kutta; returns (S, I, R) once per day."""
    s, i, r = p.initial()
    n, h = float(p.population), 1.0 / steps_per_day
    out = [(s, i, r)]
    for _day in range(days):
        for _ in range(steps_per_day):
            k1 = _derivatives(s, i, p.beta, p.gamma, n)
            k2 = _derivatives(s + h / 2 * k1[0], i + h / 2 * k1[1], p.beta, p.gamma, n)
            k3 = _derivatives(s + h / 2 * k2[0], i + h / 2 * k2[1], p.beta, p.gamma, n)
            k4 = _derivatives(s + h * k3[0], i + h * k3[1], p.beta, p.gamma, n)
            s += h / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
            i += h / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
            r += h / 6 * (k1[2] + 2 * k2[2] + 2 * k3[2] + k4[2])
        out.append((s, i, r))
    return out


def final_size(r0: float, tol: float = 1e-12) -> float:
    """Solve z = 1 − exp(−R0·z) with Newton's method: the share of the city ever infected."""
    if r0 <= 1:
        return 0.0
    z = 0.9
    for _ in range(100):
        f, df = z - 1 + math.exp(-r0 * z), 1 - r0 * math.exp(-r0 * z)
        step = f / df
        z -= step
        if abs(step) < tol:
            break
    return z


def herd_immunity_threshold(r0: float) -> float:
    return max(0.0, 1 - 1 / r0)


def sweep_numpy(betas: np.ndarray, gamma: float, population: int = 100_000, infected: int = 10,
                days: int = 365, steps_per_day: int = 10) -> dict[str, np.ndarray]:
    """Integrate one SIR model per beta *simultaneously* (RK4 on whole arrays)."""
    betas = np.asarray(betas, dtype=np.float64)
    n, h = float(population), 1.0 / steps_per_day
    s = np.full_like(betas, population - infected)
    i = np.full_like(betas, float(infected))
    peak, peak_day = i.copy(), np.zeros_like(betas)

    def deriv(s: np.ndarray, i: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        new = betas * s * i / n
        return -new, new - gamma * i

    for day in range(1, days + 1):
        for _ in range(steps_per_day):
            a1, b1 = deriv(s, i)
            a2, b2 = deriv(s + h / 2 * a1, i + h / 2 * b1)
            a3, b3 = deriv(s + h / 2 * a2, i + h / 2 * b2)
            a4, b4 = deriv(s + h * a3, i + h * b3)
            s = s + h / 6 * (a1 + 2 * a2 + 2 * a3 + a4)
            i = i + h / 6 * (b1 + 2 * b2 + 2 * b3 + b4)
        higher = i > peak
        peak = np.where(higher, i, peak)
        peak_day = np.where(higher, day, peak_day)
    return {"beta": betas, "r0": betas / gamma, "peak": peak, "peak_day": peak_day,
            "attack_rate": 1 - s / n}  # ever infected = everyone no longer susceptible


def chain_binomial(p: SIRParams, runs: int = 1000, days: int = 365, seed: int = 98) -> np.ndarray:
    """Stochastic SIR: every day each S is infected with prob 1−exp(−βI/N); returns final sizes per run."""
    rng = np.random.default_rng(seed)
    s0, i0, _ = p.initial()
    s = np.full(runs, int(round(s0)), dtype=np.int64)
    i = np.full(runs, p.infected, dtype=np.int64)
    p_recover = 1 - math.exp(-p.gamma)
    for _day in range(days):
        if not i.any():
            break  # every run has died out
        p_infect = 1 - np.exp(-p.beta * i / p.population)
        new_inf = rng.binomial(s, p_infect)
        new_rec = rng.binomial(i, p_recover)
        s -= new_inf
        i += new_inf - new_rec
    return int(round(s0)) - s + p.infected  # everyone ever infected (incl. index cases)


def summarise_runs(final_sizes: np.ndarray, population: int, major: float = 0.05) -> dict[str, Any]:
    """Mean, 95 % percentile interval, and the probability that an outbreak becomes major."""
    shares = np.asarray(final_sizes, dtype=np.float64) / population
    is_major = shares >= major
    big = shares[is_major]
    p = float(is_major.mean())
    stderr = math.sqrt(p * (1 - p) / len(shares)) if len(shares) else 0.0
    return {
        "p_major": round(p, 3),
        "p_major_ci": (round(max(0.0, p - 1.96 * stderr), 3), round(min(1.0, p + 1.96 * stderr), 3)),
        "mean_major_share": round(float(big.mean()), 3) if big.size else 0.0,
        "major_share_95": (round(float(np.percentile(big, 2.5)), 3), round(float(np.percentile(big, 97.5)), 3))
        if big.size else (0.0, 0.0),
    }


def main() -> None:
    print("Day 98 – Outbreak simulator\n")
    params = SIRParams(beta=0.3, gamma=0.1)
    days = simulate_rk4(params, days=200)
    peak_day = max(range(len(days)), key=lambda d: days[d][1])
    print(f"R0 = {params.r0:.1f}, peak on day {peak_day} with {days[peak_day][1]:,.0f} infected")
    print(f"attack rate: simulated {days[-1][2] / params.population:.3f}, analytical {final_size(params.r0):.3f}")
    print(f"herd-immunity threshold: {herd_immunity_threshold(params.r0):.0%}")
    sweep = sweep_numpy(np.linspace(0.05, 0.5, 10), gamma=0.1, days=200, steps_per_day=4)
    for r0, peak, rate in zip(sweep["r0"], sweep["peak"], sweep["attack_rate"], strict=True):
        print(f"  R0 {r0:4.1f}: peak {peak:8,.0f}  attack rate {rate:.2f}")
    single = SIRParams(beta=0.2, gamma=0.1, population=10_000, infected=1)
    print("Monte Carlo (1 index case, R0 = 2):", summarise_runs(chain_binomial(single, runs=2000), 10_000))


if __name__ == "__main__":
    main()
