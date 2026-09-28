"""
Day 63 – Browser Automation with Selenium WebDriver
Element locators, waits, form interactions, headless mode.
Falls back gracefully when Selenium / browser drivers are not available.
"""

from __future__ import annotations

import sys
import time
from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class SearchResult:
    title: str
    url: str


def selenium_available() -> bool:
    try:
        from selenium import webdriver  # noqa: F401
        from selenium.webdriver.chrome.options import Options  # noqa: F401
        return True
    except ImportError:
        return False


def create_driver(*, headless: bool = True):
    """Create a Chrome WebDriver with sensible defaults."""
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service

    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280,800")
    options.add_argument(
        "--user-agent=ProPythonMastery/1.0 (educational Selenium; Day 63)"
    )

    # Prefer Selenium Manager (Selenium 4.6+) which auto-downloads drivers
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(30)
    return driver


def demo_quotes_site(driver) -> list[SearchResult]:
    """
    Navigate to quotes.toscrape.com, wait for content,
    extract a few quotes using different locator strategies.
    """
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    url = "https://quotes.toscrape.com"
    print(f"Navigating to {url}")
    driver.get(url)

    # Explicit wait for the first quote
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.quote")))

    results: list[SearchResult] = []
    quotes = driver.find_elements(By.CSS_SELECTOR, "div.quote")
    for q in quotes[:5]:
        text_el = q.find_element(By.CSS_SELECTOR, "span.text")
        author_el = q.find_element(By.CSS_SELECTOR, "small.author")
        title = f"{text_el.text[:60]}… — {author_el.text}"
        # There is no real "url" per quote; we just use the page
        results.append(SearchResult(title=title, url=url))

    return results


def demo_form_interaction(driver) -> None:
    """Demonstrate filling a search form (DuckDuckGo) and waiting."""
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    print("\nForm interaction demo (DuckDuckGo)")
    driver.get("https://duckduckgo.com")

    wait = WebDriverWait(driver, 10)
    search_box = wait.until(EC.element_to_be_clickable((By.NAME, "q")))
    search_box.clear()
    search_box.send_keys("Python Selenium WebDriver")
    search_box.send_keys(Keys.RETURN)

    # Wait for results
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "article, .result")))
    print("  Search submitted and results appeared")
    time.sleep(1)  # brief pause so the user can see it in non-headless mode


def run_live_demo(*, headless: bool = True) -> None:
    driver = None
    try:
        driver = create_driver(headless=headless)
        print(f"Browser started (headless={headless})")

        results = demo_quotes_site(driver)
        print(f"\nExtracted {len(results)} quotes:")
        for i, r in enumerate(results, 1):
            print(f"  {i}. {r.title}")

        demo_form_interaction(driver)
        print("\n✅ Live Selenium demo finished successfully")
    finally:
        if driver is not None:
            driver.quit()
            print("Browser closed")


def run_dry_run() -> None:
    """Explain what the live demo would do when Selenium is unavailable."""
    print("Selenium / ChromeDriver not available – running dry-run explanation.")
    print()
    print("Typical workflow demonstrated on Day 63:")
    print("  1. Create Chrome options (headless, user-agent, window size)")
    print("  2. driver = webdriver.Chrome(options=options)")
    print("  3. driver.get(url)")
    print("  4. WebDriverWait + expected_conditions for robust waits")
    print("  5. find_element / find_elements with By.CSS_SELECTOR, By.NAME, etc.")
    print("  6. Interact: send_keys, click, submit")
    print("  7. Always driver.quit() in a finally block")
    print()
    print("Install tips:")
    print("  pip install selenium")
    print("  # Selenium 4.6+ ships with Selenium Manager (auto driver download)")
    print("  # Or install chromedriver / geckodriver manually")


def main() -> None:
    print("=" * 60)
    print("Day 63 – Browser Automation with Selenium")
    print("=" * 60)

    if selenium_available():
        # Prefer headless for CI / servers; set headless=False to watch the browser
        run_live_demo(headless=True)
    else:
        run_dry_run()

    print("\nKey takeaways:")
    print("• Prefer explicit waits (WebDriverWait) over time.sleep")
    print("• CSS selectors and data-testid attributes are the most stable locators")
    print("• Always quit the driver to avoid zombie processes")
    print("• Headless mode is essential for CI pipelines")
    print("• Respect robots.txt and site terms of service")

    print("\n✅ Day 63 complete")


if __name__ == "__main__":
    main()
    sys.exit(0)
