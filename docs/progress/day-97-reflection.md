# Day 97 – Automation Bot Suite Reflection

**Date:** 2026-10-01 · **Level:** Capstone · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_97_automation_bot_suite/main.py`](../../src/day_97_automation_bot_suite/main.py) · **Tests:** [`tests/test_day_97.py`](../../tests/test_day_97.py) (10 tests)

## Scenario
An *apartment-hunting bot*. Every few minutes it scrapes a listings site (politely: ``robots.txt``, paging, a delay), enriches each new flat with commute time from a JSON API, filters by the user's criteria, remembers what it has already reported, and posts matches to a chat webhook with retries – combining the scraping, API, scheduling and notification skills of the course into one pipeline.

## Syllabus deliverables
> Combining scraping, APIs, scheduling, and notifications

| Deliverable | Implemented in |
|---|---|
| ✅ polite scraper with pagination | `Scraper.listings` |
| ✅ robots.txt check | `Scraper.allowed` |
| ✅ API enrichment | `commute_minutes` |
| ✅ criteria filter | `Criteria.matches` |
| ✅ persistent de-duplication | `SeenStore` |
| ✅ webhook notification with retries | `notify` |
| ✅ scheduled run | `schedule_bot` |
| ✅ one complete bot run | `run_once` |

## Key learnings
- A bot is a pipeline: scrape → enrich via API → filter → de-duplicate → notify.
- Polite scraping respects `robots.txt`, identifies itself and pauses between pages.
- Only mark an item as seen after the notification succeeds, so failures are retried on the next run.

## Pitfalls I hit (and how I fixed them)
- Retrying 4xx errors never helps – only server errors and timeouts deserve a retry.

## Run it
```bash
python -m src.day_97_automation_bot_suite.main
pytest tests/test_day_97.py -v
```

## Next step
- Simulate an epidemic with NumPy on Day 98.
