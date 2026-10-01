# Day 63 – Browser Automation with Selenium Reflection

**Date:** 2026-09-29 · **Level:** Advanced · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_63_browser_automation_selenium/main.py`](../../src/day_63_browser_automation_selenium/main.py) · **Tests:** [`tests/test_day_63.py`](../../tests/test_day_63.py) (9 tests)

## Scenario
A *QA smoke test* for quotes.toscrape.com (a practice site): log in through the form, read quotes from the JavaScript-rendered page that appears only after a delay, and page through results – using Page Objects.

## Syllabus deliverables
> Locator strategies, waits, form filling and dynamic page interactions

| Deliverable | Implemented in |
|---|---|
| ✅ locator strategies | `LOCATORS` |
| ✅ explicit waits | `LoginPage.login` |
| ✅ form filling | `LoginPage.login` |
| ✅ dynamic (JS-rendered, delayed) content | `QuotesPage.read_quotes` |
| ✅ pagination clicks | `QuotesPage.next_page` |
| ✅ driver factory (headless) | `create_driver` |
| ✅ graceful fallback | `run` |

## Key learnings
- Prefer explicit waits (`WebDriverWait` + expected conditions) to `time.sleep`.
- Page Objects keep selectors in one place and tests readable.
- Wait for the old element to go stale to know a click really loaded a new page.

## Pitfalls I hit (and how I fixed them)
- A missing browser crashed the old demo even though it promised a dry run.

## Run it
```bash
python -m src.day_63_browser_automation_selenium.main
pytest tests/test_day_63.py -v
```

## Next step
- Run the smoke test on a schedule with screenshots on failure (Day 97).
