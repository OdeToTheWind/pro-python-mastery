"""Day 62 – Web Scraping with Beautiful Soup.

Scenario: a *quotes research assistant* that collects quotes and authors from
quotes.toscrape.com – a site built for scraping practice – *politely*.

Deliverables (syllabus):
* HTML parsing (BeautifulSoup tree, text extraction, attributes)
* Selectors (CSS selectors via ``select``/``select_one``)
* Ethical data extraction (robots.txt, identifying User-Agent, rate limiting,
  page limits, no personal data)
"""

from __future__ import annotations

import time
from collections import Counter
from collections.abc import Callable
from dataclasses import dataclass, field
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser

import requests
from bs4 import BeautifulSoup

DELIVERABLES: dict[str, str] = {
    "HTML parsing": "parse_page",
    "CSS selectors": "parse_page",
    "following pagination links": "parse_page",
    "robots.txt compliance": "PoliteFetcher.allowed",
    "rate limiting": "PoliteFetcher.fetch",
    "identifying User-Agent": "USER_AGENT",
    "aggregation of scraped data": "top_tags",
}

BASE_URL = "https://quotes.toscrape.com/"
USER_AGENT = "ProPythonMastery-Day62/1.0 (learning project; contact via GitHub issues)"


@dataclass(frozen=True, slots=True)
class Quote:
    text: str
    author: str
    tags: tuple[str, ...]
    author_url: str | None = None


def parse_page(html: str, page_url: str) -> tuple[list[Quote], str | None]:
    """Parse *one* page once: return its quotes and the absolute next-page URL."""
    soup = BeautifulSoup(html, "html.parser")
    quotes = []
    for block in soup.select("div.quote"):
        text = block.select_one("span.text")
        author = block.select_one("small.author")
        if text is None or author is None:
            continue
        link = block.select_one('a[href^="/author/"]')
        href = link.get("href") if link else None
        quotes.append(Quote(
            text=text.get_text(strip=True).strip("“”\""),
            author=author.get_text(strip=True),
            tags=tuple(tag.get_text(strip=True) for tag in block.select("div.tags a.tag")),
            author_url=urljoin(page_url, href) if isinstance(href, str) else None,
        ))
    next_link = soup.select_one("li.next > a[href]")
    next_href = next_link.get("href") if next_link else None
    return quotes, urljoin(page_url, next_href) if isinstance(next_href, str) else None


@dataclass
class PoliteFetcher:
    """Fetches pages only if robots.txt allows it, waiting between requests."""

    session: requests.Session
    delay: float = 1.0
    sleep: Callable[[float], None] = time.sleep
    clock: Callable[[], float] = time.monotonic
    _robots: dict[str, RobotFileParser] = field(default_factory=dict)
    _last: float | None = None

    def allowed(self, url: str) -> bool:
        parts = urlparse(url)
        origin = f"{parts.scheme}://{parts.netloc}"
        if origin not in self._robots:
            parser = RobotFileParser()
            try:
                response = self.session.get(f"{origin}/robots.txt", timeout=10)
                lines = response.text.splitlines() if response.status_code == 200 else []
            except requests.RequestException:
                lines = []  # unreachable robots.txt → treated as "no rules"
            parser.parse(lines)
            self._robots[origin] = parser
        return self._robots[origin].can_fetch(USER_AGENT, url)

    def fetch(self, url: str) -> str:
        if not self.allowed(url):
            raise PermissionError(f"robots.txt disallows {url}")
        if self._last is not None:
            wait = self.delay - (self.clock() - self._last)
            if wait > 0:
                self.sleep(wait)
        response = self.session.get(url, headers={"User-Agent": USER_AGENT}, timeout=10)
        self._last = self.clock()
        response.raise_for_status()
        return response.text


def scrape(fetcher: PoliteFetcher, start: str = BASE_URL, max_pages: int = 3) -> list[Quote]:
    quotes: list[Quote] = []
    url: str | None = start
    for _ in range(max_pages):
        if url is None:
            break
        page_quotes, url = parse_page(fetcher.fetch(url), url)
        quotes.extend(page_quotes)
    return quotes


def top_tags(quotes: list[Quote], n: int = 5) -> list[tuple[str, int]]:
    return Counter(tag for q in quotes for tag in q.tags).most_common(n)


def main() -> None:  # pragma: no cover – live network demo
    print("Day 62 – Polite quote scraper (live)\n")
    with requests.Session() as session:
        quotes = scrape(PoliteFetcher(session, delay=1.0), max_pages=2)
    print(f"Collected {len(quotes)} quotes")
    for quote in quotes[:3]:
        print(f"“{quote.text[:60]}” — {quote.author}")
    print("Top tags:", top_tags(quotes))


if __name__ == "__main__":  # pragma: no cover
    main()
