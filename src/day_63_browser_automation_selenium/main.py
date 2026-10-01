"""Day 63 – Browser Automation with Selenium.

Scenario: a *QA smoke test* for quotes.toscrape.com (a practice site): log in
through the form, read quotes from the JavaScript-rendered page that appears
only after a delay, and page through results – using Page Objects.

Deliverables (syllabus):
* Locator strategies (ID, NAME, CSS selector, XPath, link text)
* Waits (explicit ``WebDriverWait`` + expected conditions; no ``time.sleep``)
* Form filling (clear, type, submit, verify)
* Dynamic page interactions (JS-rendered content, pagination)
* Graceful fallback when no browser/driver is available
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

DELIVERABLES: dict[str, str] = {
    "locator strategies": "LOCATORS",
    "explicit waits": "LoginPage.login",
    "form filling": "LoginPage.login",
    "dynamic (JS-rendered, delayed) content": "QuotesPage.read_quotes",
    "pagination clicks": "QuotesPage.next_page",
    "driver factory (headless)": "create_driver",
    "graceful fallback": "run",
}

BASE_URL = "https://quotes.toscrape.com"

# (strategy, value) pairs – the same tuples Selenium's ``By`` API expects.
LOCATORS: dict[str, tuple[str, str]] = {
    "username": ("id", "username"),
    "password": ("name", "password"),
    "submit": ("css selector", "input[type='submit']"),
    "logout": ("link text", "Logout"),
    "quote": ("css selector", "div.quote"),
    "quote_text": ("css selector", "span.text"),
    "quote_author": ("xpath", ".//small[@class='author']"),
    "next": ("css selector", "li.next > a"),
}


@dataclass(frozen=True, slots=True)
class ScrapedQuote:
    text: str
    author: str


class LoginPage:
    """Page Object: tests talk to *pages*, not to raw selectors."""

    path = "/login"

    def __init__(self, driver: Any, wait: Any, ec: Any) -> None:
        self.driver, self.wait, self.ec = driver, wait, ec

    def open(self) -> LoginPage:
        self.driver.get(BASE_URL + self.path)
        return self

    def login(self, username: str, password: str) -> bool:
        user = self.wait.until(self.ec.element_to_be_clickable(LOCATORS["username"]))
        user.clear()
        user.send_keys(username)
        pwd = self.driver.find_element(*LOCATORS["password"])
        pwd.clear()
        pwd.send_keys(password)
        self.driver.find_element(*LOCATORS["submit"]).click()
        self.wait.until(self.ec.presence_of_element_located(LOCATORS["logout"]))
        return True


class QuotesPage:
    def __init__(self, driver: Any, wait: Any, ec: Any) -> None:
        self.driver, self.wait, self.ec = driver, wait, ec

    def open_delayed(self) -> QuotesPage:
        """``/js-delayed/`` renders quotes with JavaScript after ~10 s."""
        self.driver.get(f"{BASE_URL}/js-delayed/")
        return self

    def read_quotes(self) -> list[ScrapedQuote]:
        self.wait.until(self.ec.presence_of_all_elements_located(LOCATORS["quote"]))
        quotes = []
        for element in self.driver.find_elements(*LOCATORS["quote"]):
            text = element.find_element(*LOCATORS["quote_text"]).text.strip("“”")
            author = element.find_element(*LOCATORS["quote_author"]).text
            quotes.append(ScrapedQuote(text, author))
        return quotes

    def next_page(self) -> bool:
        links = self.driver.find_elements(*LOCATORS["next"])
        if not links:
            return False
        first_quote = self.driver.find_elements(*LOCATORS["quote"])[0]
        links[0].click()
        self.wait.until(self.ec.staleness_of(first_quote))  # old page gone → new page loaded
        return True


def create_driver(headless: bool = True) -> Any:
    from selenium import webdriver

    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1280,900")
    driver = webdriver.Chrome(options=options)  # Selenium Manager finds/downloads the driver
    driver.set_page_load_timeout(30)
    return driver


def smoke_test(driver: Any, wait: Any, ec: Any, pages: int = 2) -> list[ScrapedQuote]:
    LoginPage(driver, wait, ec).open().login("demo-user", "demo-pass")  # practice site accepts any login
    page = QuotesPage(driver, wait, ec).open_delayed()
    quotes = page.read_quotes()
    while pages > 1 and page.next_page():
        quotes += page.read_quotes()
        pages -= 1
    return quotes


DRY_RUN_STEPS = (
    "driver = webdriver.Chrome(options=headless_options)",
    "LoginPage.open() → wait until #username is clickable → type credentials → submit",
    "wait until the 'Logout' link exists (proves login worked)",
    "open /js-delayed/ → wait for all div.quote elements (rendered by JavaScript)",
    "click 'Next' → wait for the old quote element to become stale",
    "driver.quit() in a finally block",
)


def run(headless: bool = True) -> str:
    """Run the live smoke test, or explain the steps if no browser is available."""
    try:
        from selenium.common.exceptions import WebDriverException
        from selenium.webdriver.support import expected_conditions as ec
        from selenium.webdriver.support.ui import WebDriverWait
    except ImportError:
        return "dry-run: selenium is not installed\n  " + "\n  ".join(DRY_RUN_STEPS)
    try:
        driver = create_driver(headless)
    except WebDriverException as exc:
        reason = str(exc).splitlines()[0][:80]
        return f"dry-run: no browser/driver available ({reason})\n  " + "\n  ".join(DRY_RUN_STEPS)
    try:
        quotes = smoke_test(driver, WebDriverWait(driver, 15), ec)
        return f"live: {len(quotes)} quotes, first by {quotes[0].author if quotes else 'nobody'}"
    except WebDriverException as exc:
        return f"failed: {type(exc).__name__}: {str(exc).splitlines()[0][:80]}"
    finally:
        driver.quit()


def main() -> None:  # pragma: no cover – may launch a browser
    print("Day 63 – Selenium smoke test\n")
    print(run())


if __name__ == "__main__":  # pragma: no cover
    main()
