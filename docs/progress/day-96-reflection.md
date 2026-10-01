# Day 96 – Packaging a Real Tool Reflection

**Date:** 2026-10-01 · **Level:** Capstone · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_96_packaging_real_tool/main.py`](../../src/day_96_packaging_real_tool/main.py) · **Tests:** [`tests/test_day_96.py`](../../tests/test_day_96.py) (13 tests)

## Scenario
Ship ``tidyfiles`` – a *downloads-folder organiser* that sorts files into ``images/``, ``documents/``, ``archives/`` … – as a release-ready project. Day 79 learned the packaging mechanics; today is the **release engineering** around a working tool: the tool's code is single-sourced into the package, usage docs are generated from the real ``argparse`` parser, the project ships its own tests, versions are bumped with a changelog, a pre-flight check blocks incomplete releases, and a GitHub Actions workflow publishes to TestPyPI with trusted publishing (no API token stored).

## Syllabus deliverables
> Complete pyproject.toml, CLI entry point, documentation, tests, and TestPyPI publishing

| Deliverable | Implemented in |
|---|---|
| ✅ the real tool: plan and apply moves | `plan_moves` |
| ✅ CLI entry point | `cli` |
| ✅ complete pyproject.toml | `render_pyproject` |
| ✅ docs generated from the parser | `usage_markdown` |
| ✅ semantic version bump + changelog | `bump_version` |
| ✅ project scaffold with shipped tests | `scaffold` |
| ✅ release pre-flight checks | `preflight` |
| ✅ TestPyPI trusted-publishing workflow | `PUBLISH_WORKFLOW` |

## Key learnings
- Single-source the tool's code and generate the docs from the real parser, so they never drift apart.
- A pre-flight check blocks releases that lack a changelog entry, licence, tests or up-to-date docs.
- Trusted publishing (`id-token: write`) uploads to TestPyPI without storing an API token.

## Pitfalls I hit (and how I fixed them)
- Bumping the version without a matching changelog entry confuses users about what changed.

## Run it
```bash
python -m src.day_96_packaging_real_tool.main
pytest tests/test_day_96.py -v
```

## Next step
- Combine scraping, APIs, scheduling and notifications on Day 97.
