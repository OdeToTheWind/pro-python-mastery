# Day 42 – File Directories Reflection

**Date:** 2026-04-23 · **Level:** Intermediate · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_42_file_directories/main.py`](../../src/day_42_file_directories/main.py) · **Tests:** [`tests/test_day_42.py`](../../tests/test_day_42.py) (9 tests)

## Scenario
A *downloads-folder organiser* – it scaffolds folders, prints a tree, finds files by pattern, sorts files into folders by extension and cleans up, all confined to one sandbox root so a typo can never touch the rest of the disk.

## Syllabus deliverables
> os and pathlib, folder navigation and file system work

| Deliverable | Implemented in |
|---|---|
| ✅ os vs pathlib | `list_with_os_and_pathlib` |
| ✅ navigation: tree listing | `tree` |
| ✅ navigation: os.walk | `folder_sizes` |
| ✅ navigation: glob / rglob | `find_files` |
| ✅ file-system work: create | `create_folder` |
| ✅ file-system work: move | `organise_by_extension` |
| ✅ file-system work: safe removal | `remove_folder` |
| ✅ path traversal protection | `inside` |

## Key learnings
- `pathlib` reads better than `os.path` for most work; `os.walk` is still handy for full traversals.
- Resolve and check `is_relative_to(root)` to block `../` path traversal.
- Destructive operations should need explicit consent (`recursive=True`).

## Pitfalls I hit (and how I fixed them)
- `os.rmdir` on a non-empty folder raised an unhandled `OSError` in the original version.

## Run it
```bash
python -m src.day_42_file_directories.main
pytest tests/test_day_42.py -v
```

## Next step
- Combine globbing and generators in the ETL pipeline (Day 84).
