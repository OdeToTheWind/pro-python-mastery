# Day 71 – Functional Tools Reflection

**Date:** 2026-10-01 · **Level:** Advanced · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_71_functional_tools/main.py`](../../src/day_71_functional_tools/main.py) · **Tests:** [`tests/test_day_71.py`](../../tests/test_day_71.py) (12 tests)

## Scenario
A *music-streaming royalty calculator* – play logs are grouped, accumulated and combined with ``itertools``; pricing rules are pre-configured with ``partial``; expensive look-ups are cached with ``lru_cache``; totals are folded with ``reduce``.

## Syllabus deliverables
> itertools, functools, partial, lru\_cache, and reduce

| Deliverable | Implemented in |
|---|---|
| ✅ itertools.groupby | `plays_per_artist` |
| ✅ itertools.accumulate | `running_streams` |
| ✅ itertools.chain / islice | `merge_playlists` |
| ✅ itertools.pairwise | `skip_detector` |
| ✅ itertools.batched | `payout_batches` |
| ✅ itertools.combinations | `collab_pairs` |
| ✅ functools.partial | `royalty_for` |
| ✅ functools.lru\_cache | `artist_rate` |
| ✅ functools.reduce | `total_payout` |
| ✅ functools.singledispatch | `describe` |
| ✅ functools.total\_ordering | `Track` |

## Key learnings
- `partial` freezes arguments to create specialised functions without writing wrappers.
- `lru_cache` turns repeated expensive calls into dictionary look-ups; `cache_info()` shows hits and misses.
- `itertools` tools are lazy building blocks: `groupby` needs sorted input, `accumulate` gives running totals, `pairwise`/`batched` slice streams.

## Pitfalls I hit (and how I fixed them)
- `groupby` only groups *consecutive* equal keys – forgetting to sort first silently splits groups.

## Run it
```bash
./propython.sh 71                 # study mode: explanation, code map, notes and tests
python -m src.day_71_functional_tools.main
pytest tests/test_day_71.py -v
```

## Next step
- Describe these functions precisely with Protocols and generics on Day 72.
