"""Tests for Day 63 – Selenium (a fake driver stands in for the browser)."""

import sys
import types

import pytest
from selenium.common.exceptions import WebDriverException

from src.day_63_browser_automation_selenium import main as day63
from src.day_63_browser_automation_selenium.main import (
    LOCATORS,
    LoginPage,
    QuotesPage,
    ScrapedQuote,
    run,
    smoke_test,
)


class FakeElement:
    def __init__(self, text="", children=None):
        self.text, self.children, self.typed, self.clicked, self.cleared = text, children or {}, [], False, False

    def clear(self):
        self.cleared = True

    def send_keys(self, value):
        self.typed.append(value)

    def click(self):
        self.clicked = True

    def find_element(self, by, value):
        return self.children[(by, value)]


def quote_el(text, author):
    return FakeElement(children={LOCATORS["quote_text"]: FakeElement(f"“{text}”"),
                                 LOCATORS["quote_author"]: FakeElement(author)})


class FakeDriver:
    def __init__(self, pages):
        self.pages, self.page_index, self.visited, self.quit_called = pages, 0, [], False
        self.fields = {LOCATORS["username"]: FakeElement(), LOCATORS["password"]: FakeElement(),
                       LOCATORS["submit"]: FakeElement()}
        self.next_link = FakeElement()

    def get(self, url):
        self.visited.append(url)

    def find_element(self, by, value):
        return self.fields[(by, value)]

    def find_elements(self, by, value):
        if (by, value) == LOCATORS["quote"]:
            return self.pages[self.page_index]
        if (by, value) == LOCATORS["next"]:
            return [self.next_link] if self.page_index < len(self.pages) - 1 else []
        return []

    def quit(self):
        self.quit_called = True


class FakeWait:
    def __init__(self, driver):
        self.driver, self.conditions = driver, []

    def until(self, condition):
        self.conditions.append(condition[0])
        if condition[0] == "stale":
            self.driver.page_index += 1
        if condition[0] == "clickable":
            return self.driver.fields[condition[1]]
        return True


FakeEC = types.SimpleNamespace(
    element_to_be_clickable=lambda loc: ("clickable", loc),
    presence_of_element_located=lambda loc: ("present", loc),
    presence_of_all_elements_located=lambda loc: ("all_present", loc),
    staleness_of=lambda el: ("stale", el),
)


@pytest.fixture
def driver():
    return FakeDriver([[quote_el("A", "Ada"), quote_el("B", "Bob")], [quote_el("C", "Cy")]])


def test_locators_use_several_strategies():
    strategies = {by for by, _ in LOCATORS.values()}
    assert {"id", "name", "css selector", "xpath", "link text"} <= strategies


def test_login_fills_form_with_explicit_waits(driver):
    wait = FakeWait(driver)
    assert LoginPage(driver, wait, FakeEC).open().login("u", "p")
    assert driver.visited == ["https://quotes.toscrape.com/login"]
    assert driver.fields[LOCATORS["username"]].typed == ["u"] and driver.fields[LOCATORS["username"]].cleared
    assert driver.fields[LOCATORS["password"]].typed == ["p"]
    assert driver.fields[LOCATORS["submit"]].clicked
    assert wait.conditions == ["clickable", "present"]


def test_read_quotes_waits_for_dynamic_content(driver):
    wait = FakeWait(driver)
    assert QuotesPage(driver, wait, FakeEC).read_quotes() == [ScrapedQuote("A", "Ada"), ScrapedQuote("B", "Bob")]
    assert wait.conditions == ["all_present"]


def test_next_page_waits_for_staleness(driver):
    page = QuotesPage(driver, FakeWait(driver), FakeEC)
    assert page.next_page() is True and driver.next_link.clicked
    assert page.next_page() is False


def test_smoke_test_collects_all_pages(driver):
    quotes = smoke_test(driver, FakeWait(driver), FakeEC, pages=5)
    assert [q.author for q in quotes] == ["Ada", "Bob", "Cy"]


def test_run_falls_back_when_browser_missing(monkeypatch):
    def broken_driver(headless=True):
        raise WebDriverException("Message: chrome not found")

    monkeypatch.setattr(day63, "create_driver", broken_driver)
    result = run()
    assert result.startswith("dry-run: no browser/driver available")
    assert "driver.quit()" in result


def test_run_live_path_always_quits(monkeypatch, driver):
    monkeypatch.setattr(day63, "create_driver", lambda headless=True: driver)
    monkeypatch.setattr(day63, "smoke_test", lambda d, w, e: [ScrapedQuote("x", "Ada")])
    assert run() == "live: 1 quotes, first by Ada"
    assert driver.quit_called


def test_run_reports_failures_and_quits(monkeypatch, driver):
    def failing(*_args):
        raise WebDriverException("Message: timeout")

    monkeypatch.setattr(day63, "create_driver", lambda headless=True: driver)
    monkeypatch.setattr(day63, "smoke_test", failing)
    assert run().startswith("failed: WebDriverException")
    assert driver.quit_called


def test_run_without_selenium(monkeypatch):
    monkeypatch.setitem(sys.modules, "selenium.common.exceptions", None)
    assert run().startswith("dry-run: selenium is not installed")
