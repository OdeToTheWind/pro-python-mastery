# Day 90 – Memory-efficient Large File Processor Reflection

**Date:** 2026-10-01 · **Level:** Capstone · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_90_memory_efficient_file_processor/main.py`](../../src/day_90_memory_efficient_file_processor/main.py) · **Tests:** [`tests/test_day_90.py`](../../tests/test_day_90.py) (9 tests)

## Scenario
A *DNA-sequencing lab* receives FASTQ files far larger than RAM. Reads are streamed in fixed-size binary chunks, re-assembled into lines and 4-line records, quality-filtered, counted, and sorted with an *external* merge sort – and ``tracemalloc`` proves the peak memory stays flat while the file grows.

## Syllabus deliverables
> Generators, streaming, and chunking

| Deliverable | Implemented in |
|---|---|
| ✅ fixed-size chunk reader | `read_chunks` |
| ✅ lines across chunk borders | `lines_from_chunks` |
| ✅ streaming record parser | `parse_fastq` |
| ✅ quality filter pipeline | `filter_reads` |
| ✅ single-pass statistics | `stream_stats` |
| ✅ external merge sort | `external_sort` |
| ✅ mmap pattern search | `mmap_count` |
| ✅ peak memory measurement | `peak_memory` |

## Key learnings
- Reading fixed-size chunks and gluing the tail of each chunk to the next keeps memory flat at any file size.
- An external merge sort sorts more data than fits in RAM: sorted runs on disk plus `heapq.merge`.
- `tracemalloc` proves the streaming version's peak memory does not grow with the input.

## Pitfalls I hit (and how I fixed them)
- Lines from a file keep their newline – strip them before parsing, or records shift silently.

## Run it
```bash
python -m src.day_90_memory_efficient_file_processor.main
pytest tests/test_day_90.py -v
```

## Next step
- Build a type-safe configuration system on Day 91.
