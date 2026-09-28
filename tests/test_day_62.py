"""Tests for Day 62 – Web Scraping with Beautiful Soup."""

from __future__ import annotations

from unittest.mock import patch

import pytest

from src.day_62_web_scraping.main import (
    Quote,
    get_next_page_url,
    parse_quotes,
    scrape_quotes,
)


SAMPLE_HTML = """
<html>
<body>
  <div class="quote">
    <span class="text">“The world as we have created it is a process of our thinking.”</span>
    <span>by <small class="author">Albert Einstein</small></span>
    <div class="tags">
      <a class="tag" href="/tag/change/page/1/">change</a>
      <a class="tag" href="/tag/deep-thoughts/page/1/">deep-thoughts</a>
    </div>
  </div>
  <div class="quote">
    <span class="text">“It is our choices that show what we truly are.”</span>
    <span>by <small class="author">J.K. Rowling</small></span>
    <div class="tags">
      <a class="tag" href="/tag/abilities/page/1/">abilities</a>
    </div>
  </div>
  <nav>
    <ul class="pager">
      <li class="next"><a href="/page/2/">Next →</a></li>
    </ul>
  </nav>
</body>
</html>
"""

LAST_PAGE_HTML = """
<html><body>
  <div class="quote">
    <span class="text">“Last quote.”</span>
    <small class="author">Someone</small>
    <div class="tags"></div>
  </div>
</body></html>
"""


def test_parse_quotes():
    quotes = parse_quotes(SAMPLE_HTML)
    assert len(quotes) == 2
    assert isinstance(quotes[0], Quote)
    assert "Einstein" in quotes[0].author
    assert "change" in quotes[0].tags
    assert quotes[1].author == "J.K. Rowling"


def test_parse_quotes_empty():
    assert parse_quotes("<html><body></body></html>") == []


def test_get_next_page_url():
    next_url = get_next_page_url(SAMPLE_HTML, "https://quotes.toscrape.com")
    assert next_url == "https://quotes.toscrape.com/page/2/"


def test_get_next_page_url_none():
    assert get_next_page_url(LAST_PAGE_HTML, "https://quotes.toscrape.com") is None


def test_scrape_quotes_mocked():
    with patch(
        "src.day_62_web_scraping.main.fetch_html",
        side_effect=[SAMPLE_HTML, LAST_PAGE_HTML],
    ):
        quotes = scrape_quotes(max_pages=2)
    assert len(quotes) == 3  # 2 from first page + 1 from second
    assert all(isinstance(q, Quote) for q in quotes)


def test_quote_frozen():
    q = Quote(text="hi", author="me", tags=("a",))
    with pytest.raises(Exception):  # FrozenInstanceError
        q.text = "changed"  # type: ignore[misc]
