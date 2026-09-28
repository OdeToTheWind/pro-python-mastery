# Day 62 - Web Scraping with Beautiful Soup Reflection

**Date:** 2026-09-29  
**Python Version Used:** 3.12+  
**Time Spent:** 2 hours  
**Git Commit Hash (optional):** 

## What I Built / Key Deliverables
- `Quote` frozen dataclass for structured scraped data
- Page fetcher with polite User-Agent
- CSS-selector based parser for quotes.toscrape.com
- Multi-page scraper that follows “Next” links via `urljoin`

## Core Learnings & Insights
- Beautiful Soup + CSS selectors (`select` / `select_one`) is the most readable combination
- Always set a descriptive User-Agent and respect `robots.txt`
- `urljoin` is the correct way to turn relative links into absolute ones
- Frozen dataclasses make scraped records immutable and hashable
- Limiting pages and adding delays are essential for responsible scraping

## Challenges Faced & How I Solved Them
- Handling missing elements gracefully → check for `None` before calling `.get_text()`
- Encoding issues → use `resp.apparent_encoding` as fallback

## Improvements for Next Time / Future Ideas
- Add rate-limiting / exponential back-off
- Cache pages locally to avoid re-downloading during development
- Export results to CSV / JSON with `csv` or `json` modules
- Explore Scrapy later for larger crawls

## References / Resources Used
- https://www.crummy.com/software/BeautifulSoup/bs4/doc/
- https://quotes.toscrape.com/
- https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Selectors

## Self-Assessment
- Coverage goal met? Parser and multi-page logic covered by tests (with mocked HTML)
- Typing strictness: fully typed
- Code cleanliness: pure functions, easy to unit-test
- Personal rating: 9/10 – classic and very useful skill
