# Day 98 – Scientific / Simulation Mini-project Reflection

**Date:** 2026-10-01 · **Level:** Capstone · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_98_scientific_simulation/main.py`](../../src/day_98_scientific_simulation/main.py) · **Tests:** [`tests/test_day_98.py`](../../tests/test_day_98.py) (9 tests)

## Scenario
An *epidemic outbreak simulator* for a city health department. A deterministic SIR model is integrated in pure Python (RK4) and validated against the analytical final-size equation; NumPy then sweeps hundreds of transmission rates at once, and a stochastic chain-binomial Monte Carlo answers the questions a planner actually asks: *how likely is a major outbreak, and how large could it get?*

## Syllabus deliverables
> NumPy and a pure-Python simulation or Monte Carlo project

| Deliverable | Implemented in |
|---|---|
| ✅ model parameters and R0 | `SIRParams` |
| ✅ pure-Python RK4 simulation | `simulate_rk4` |
| ✅ analytical final size (validation) | `final_size` |
| ✅ NumPy parameter sweep | `sweep_numpy` |
| ✅ stochastic Monte Carlo | `chain_binomial` |
| ✅ summary statistics with confidence intervals | `summarise_runs` |
| ✅ vaccination threshold | `herd_immunity_threshold` |

## Key learnings
- A hand-written RK4 integrator in pure Python is accurate enough to match the analytical final size.
- NumPy integrates hundreds of models at once by running the same maths on whole arrays.
- A seeded Monte Carlo answers probabilistic questions and reports confidence intervals.

## Pitfalls I hit (and how I fixed them)
- Without checks like population conservation, a simulation bug looks just like a scientific result.

## Run it
```bash
./propython.sh 98                 # study mode: explanation, code map, notes and tests
python -m src.day_98_scientific_simulation.main
pytest tests/test_day_98.py -v
```

## Next step
- Build an observability and debugging toolkit on Day 99.
