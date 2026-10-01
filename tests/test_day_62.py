"""Tests for Day 62 – Web Scraping (HTML and HTTP are faked)."""

from types import SimpleNamespace

import pytest
import requests

from src.day_62_web_scraping.main import (
    USER_AGENT,
    PoliteFetcher,
    Quote,
    parse_page,
    scrape,
    top_tags,
)

PAGE_1 = """
<div class="quote"><span class="text">“Be yourself.”</span>
  <span>by <small class="author">Oscar Wilde</small> <a href="/author/Oscar-Wilde">(about)</a></span>
  <div class="tags"><a class="tag">life</a><a class="tag">honesty</a></div></div>
<div class="quote"><span class="text">“Broken quote without author”</span></div>
<ul class="pager"><li class="next"><a href="/page/2/">Next</a></li></ul>
"""
PAGE_2 = """
<div class="quote"><span class="text">“Simplicity is ...”</span><small class="author">Leonardo</small>
  <div class="tags"><a class="tag">life</a></div></div>
"""


class FakeSession:
    def __init__(self, pages, robots="User-agent: *\nDisallow: /private\n", robots_status=200):
        self.pages, self.robots, self.robots_status, self.calls = pages, robots, robots_status, []

    def get(self, url, headers=None, timeout=None):
        self.calls.append((url, headers, timeout))
        if url.endswith("/robots.txt"):
            if self.robots_status is None:
                raise requests.ConnectionError("down")
            return SimpleNamespace(status_code=self.robots_status, text=self.robots)
        text = self.pages[url]
        return SimpleNamespace(status_code=200, text=text, raise_for_status=lambda: None)


def make_fetcher(session, waits=None, times=None):
    times = iter(times or [0.0, 0.2, 2.0, 2.5])
    return PoliteFetcher(session, delay=1.0, sleep=(waits if waits is not None else []).append,
                         clock=lambda: next(times))


def test_parse_page_extracts_quotes_and_next_link():
    quotes, next_url = parse_page(PAGE_1, "https://q.test/")
    assert quotes == [Quote("Be yourself.", "Oscar Wilde", ("life", "honesty"), "https://q.test/author/Oscar-Wilde")]
    assert next_url == "https://q.test/page/2/"


def test_parse_last_page():
    quotes, next_url = parse_page(PAGE_2, "https://q.test/page/2/")
    assert quotes[0].author_url is None and next_url is None


def test_robots_txt_is_respected():
    fetcher = make_fetcher(FakeSession({}))
    assert fetcher.allowed("https://q.test/page/1/")
    assert not fetcher.allowed("https://q.test/private/data")
    with pytest.raises(PermissionError):
        fetcher.fetch("https://q.test/private/data")


def test_robots_is_fetched_once_per_origin():
    session = FakeSession({})
    fetcher = make_fetcher(session)
    fetcher.allowed("https://q.test/a")
    fetcher.allowed("https://q.test/b")
    assert [c[0] for c in session.calls] == ["https://q.test/robots.txt"]


@pytest.mark.parametrize("status", [404, None])
def test_missing_or_unreachable_robots_allows(status):
    assert make_fetcher(FakeSession({}, robots_status=status)).allowed("https://q.test/x")


def test_fetch_waits_between_requests_and_sends_user_agent():
    session = FakeSession({"https://q.test/": PAGE_1, "https://q.test/page/2/": PAGE_2})
    waits = []
    fetcher = make_fetcher(session, waits, times=[0.0, 0.3, 1.0])
    fetcher.fetch("https://q.test/")
    fetcher.fetch("https://q.test/page/2/")
    assert waits == [pytest.approx(0.7)]
    page_calls = [c for c in session.calls if not c[0].endswith("robots.txt")]
    assert all(c[1] == {"User-Agent": USER_AGENT} and c[2] == 10 for c in page_calls)


def test_scrape_follows_pagination_with_page_limit():
    session = FakeSession({"https://q.test/": PAGE_1, "https://q.test/page/2/": PAGE_2})
    quotes = scrape(make_fetcher(session), "https://q.test/", max_pages=5)
    assert [q.author for q in quotes] == ["Oscar Wilde", "Leonardo"]
    assert len(scrape(make_fetcher(session), "https://q.test/", max_pages=1)) == 1


def test_top_tags():
    quotes = [Quote("a", "x", ("life", "love")), Quote("b", "y", ("life",))]
    assert top_tags(quotes, 1) == [("life", 2)]
