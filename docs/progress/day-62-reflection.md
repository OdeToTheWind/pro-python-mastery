# Day 62 – Web Scraping with Beautiful Soup Reflection

**Date:** 2026-09-29 · **Level:** Advanced · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_62_web_scraping/main.py`](../../src/day_62_web_scraping/main.py) · **Tests:** [`tests/test_day_62.py`](../../tests/test_day_62.py) (8 tests)

## Scenario
A *quotes research assistant* that collects quotes and authors from quotes.toscrape.com – a site built for scraping practice – *politely*.

## Syllabus deliverables
> HTML parsing, selectors and ethical data extraction

| Deliverable | Implemented in |
|---|---|
| ✅ HTML parsing | `parse_page` |
| ✅ CSS selectors | `parse_page` |
| ✅ following pagination links | `parse_page` |
| ✅ robots.txt compliance | `PoliteFetcher.allowed` |
| ✅ rate limiting | `PoliteFetcher.fetch` |
| ✅ identifying User-Agent | `USER_AGENT` |
| ✅ aggregation of scraped data | `top_tags` |

## Key learnings
- CSS selectors (`select`, `select_one`) keep extraction readable and robust.
- Respect robots.txt, identify yourself with a User-Agent and rate-limit requests.
- Parse each page once and follow pagination with `urljoin`.

## Pitfalls I hit (and how I fixed them)
- Each page used to be parsed twice, and `lxml` was installed but never used.

## Run it
```bash
python -m src.day_62_web_scraping.main
pytest tests/test_day_62.py -v
```

## Next step
- Schedule polite scraping jobs in the background task runner (Day 89).
