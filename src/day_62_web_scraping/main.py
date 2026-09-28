"""
Day 62 – Web Scraping with Beautiful Soup
Parsing HTML, navigating the DOM, extracting data, handling basic pages.
Uses a public, scraping-friendly site (quotes.toscrape.com).
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import Iterator
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


BASE_URL = "https://quotes.toscrape.com"


@dataclass(slots=True, frozen=True)
class Quote:
    text: str
    author: str
    tags: tuple[str, ...]


def fetch_html(url: str, *, timeout: float = 10.0) -> str:
    """Download page HTML with a polite User-Agent."""
    headers = {
        "User-Agent": "ProPythonMastery/1.0 (educational scraper; +https://example.com)",
        "Accept-Language": "en-US,en;q=0.9",
    }
    resp = requests.get(url, headers=headers, timeout=timeout)
    resp.raise_for_status()
    resp.encoding = resp.apparent_encoding or "utf-8"
    return resp.text


def parse_quotes(html: str) -> list[Quote]:
    """Extract quotes from a single page."""
    soup = BeautifulSoup(html, "html.parser")
    results: list[Quote] = []

    for q in soup.select("div.quote"):
        text_el = q.select_one("span.text")
        author_el = q.select_one("small.author")
        tag_els = q.select("div.tags a.tag")

        if not (text_el and author_el):
            continue

        text = text_el.get_text(strip=True).strip("“”\"")
        author = author_el.get_text(strip=True)
        tags = tuple(t.get_text(strip=True) for t in tag_els)
        results.append(Quote(text=text, author=author, tags=tags))

    return results


def get_next_page_url(html: str, current_url: str) -> str | None:
    """Return absolute URL of the next page, or None if last page."""
    soup = BeautifulSoup(html, "html.parser")
    next_link = soup.select_one("li.next > a")
    if not next_link or not next_link.get("href"):
        return None
    return urljoin(current_url, next_link["href"])


def scrape_quotes(max_pages: int = 2) -> list[Quote]:
    """Scrape up to `max_pages` pages of quotes."""
    all_quotes: list[Quote] = []
    url: str | None = BASE_URL
    page = 0

    while url and page < max_pages:
        page += 1
        print(f"Fetching page {page}: {url}")
        html = fetch_html(url)
        quotes = parse_quotes(html)
        all_quotes.extend(quotes)
        print(f"  → {len(quotes)} quotes")
        url = get_next_page_url(html, url)

    return all_quotes


def print_summary(quotes: list[Quote]) -> None:
    """Pretty-print a few results."""
    print(f"\nTotal quotes collected: {len(quotes)}")
    for i, q in enumerate(quotes[:5], 1):
        print(f"\n{i}. “{q.text[:70]}…”")
        print(f"   — {q.author}")
        print(f"   tags: {', '.join(q.tags)}")


def main() -> None:
    print("=" * 60)
    print("Day 62 – Web Scraping with Beautiful Soup")
    print("=" * 60)

    quotes = scrape_quotes(max_pages=2)
    print_summary(quotes)

    print("\nBest practices demonstrated:")
    print("• Always set a descriptive User-Agent")
    print("• Prefer CSS selectors (soup.select) for readability")
    print("• Use urljoin for relative links")
    print("• Limit pages / respect robots.txt in real projects")
    print("• Add delays (time.sleep) when scraping more aggressively")

    print("\n✅ Day 62 complete")


if __name__ == "__main__":
    main()
    sys.exit(0)
