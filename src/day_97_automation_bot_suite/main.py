"""Day 97 – Capstone: Automation Bot Suite.

Scenario: an *apartment-hunting bot*. Every few minutes it scrapes a listings
site (politely: ``robots.txt``, paging, a delay), enriches each new flat
with commute time from a JSON API, filters by the user's criteria, remembers
what it has already reported, and posts matches to a chat webhook with
retries – combining the scraping, API, scheduling and notification skills of
the course into one pipeline.

Deliverables (syllabus):
* Scraping (``requests`` + BeautifulSoup, pagination, ``robots.txt``)
* APIs (JSON enrichment with timeouts and error handling)
* Scheduling (``schedule`` job with a run summary)
* Notifications (webhook POST with retry/backoff) and de-duplicated state
"""

from __future__ import annotations

import json
import os
import tempfile
import threading
import time
import urllib.robotparser
from collections.abc import Callable, Iterator
from dataclasses import asdict, dataclass, field
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse

import requests
import schedule
from bs4 import BeautifulSoup

DELIVERABLES: dict[str, str] = {
    "polite scraper with pagination": "Scraper.listings",
    "robots.txt check": "Scraper.allowed",
    "API enrichment": "commute_minutes",
    "criteria filter": "Criteria.matches",
    "persistent de-duplication": "SeenStore",
    "webhook notification with retries": "notify",
    "scheduled run": "schedule_bot",
    "one complete bot run": "run_once",
}

USER_AGENT = "flat-hunter-bot/1.0 (+https://github.com/OdeToTheWind/pro-python-mastery)"


@dataclass(frozen=True, slots=True)
class Listing:
    listing_id: str
    title: str
    rent: int
    rooms: float
    district: str
    url: str
    commute: int | None = None


@dataclass(frozen=True)
class Criteria:
    max_rent: int
    min_rooms: float = 1
    max_commute: int = 45
    districts: frozenset[str] = frozenset()

    def matches(self, flat: Listing) -> bool:
        return (flat.rent <= self.max_rent and flat.rooms >= self.min_rooms
                and (flat.commute is not None and flat.commute <= self.max_commute)
                and (not self.districts or flat.district.lower() in self.districts))


@dataclass
class Scraper:
    base_url: str
    session: requests.Session = field(default_factory=requests.Session)
    delay: float = 0.0
    timeout: float = 5.0
    max_pages: int = 10

    def __post_init__(self) -> None:
        self.session.headers["User-Agent"] = USER_AGENT
        self._robots: urllib.robotparser.RobotFileParser | None = None

    def allowed(self, path: str) -> bool:
        if self._robots is None:
            self._robots = urllib.robotparser.RobotFileParser()
            try:
                response = self.session.get(f"{self.base_url}/robots.txt", timeout=self.timeout)
                lines = response.text.splitlines() if response.status_code == 200 else []
            except requests.RequestException:
                lines = []  # unreachable robots.txt → treat as "no rules"
            self._robots.parse(lines)
        return self._robots.can_fetch(USER_AGENT, f"{self.base_url}{path}")

    def listings(self) -> Iterator[Listing]:
        path = "/listings?page=1"
        for _page in range(self.max_pages):
            if not self.allowed(path):
                raise PermissionError(f"robots.txt disallows {path}")
            response = self.session.get(f"{self.base_url}{path}", timeout=self.timeout)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            for card in soup.select("article.listing"):
                rent = card.select_one(".rent")
                rooms = card.select_one(".rooms")
                link = card.select_one("a")
                if rent is None or rooms is None or link is None:
                    continue  # malformed card: skip, keep scraping
                yield Listing(str(card["data-id"]), link.get_text(strip=True),
                              int("".join(ch for ch in rent.get_text() if ch.isdigit())),
                              float(rooms.get_text(strip=True).split()[0]),
                              str(card.get("data-district", "")), f"{self.base_url}{link['href']}")
            nxt = soup.select_one("a[rel=next]")
            if nxt is None:
                return
            path = str(nxt["href"])
            time.sleep(self.delay)  # be polite between pages


def commute_minutes(session: requests.Session, api_url: str, listing_id: str, timeout: float = 5.0) -> int | None:
    try:
        response = session.get(f"{api_url}/commute", params={"id": listing_id}, timeout=timeout)
        response.raise_for_status()
        return int(response.json()["minutes"])
    except (requests.RequestException, KeyError, ValueError, TypeError):
        return None  # unknown commute → the flat simply won't match


class SeenStore:
    """IDs already reported, stored atomically so a crash never loses or corrupts state."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.ids: set[str] = set(json.loads(path.read_text(encoding="utf-8"))) if path.exists() else set()

    def add(self, listing_id: str) -> None:
        self.ids.add(listing_id)

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp = tempfile.mkstemp(dir=self.path.parent)
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(sorted(self.ids), handle)
        os.replace(tmp, self.path)


def notify(session: requests.Session, webhook_url: str, flat: Listing, *, retries: int = 2,
           backoff: float = 0.01, timeout: float = 5.0) -> bool:
    text = f"🏠 {flat.title} – €{flat.rent}, {flat.rooms:g} rooms, {flat.commute} min commute\n{flat.url}"
    for attempt in range(retries + 1):
        try:
            response = session.post(webhook_url, json={"text": text, "listing": asdict(flat)}, timeout=timeout)
            if response.status_code < 500:
                return response.ok  # 4xx will not get better by retrying
        except requests.RequestException:
            pass
        time.sleep(backoff * 2**attempt)
    return False


@dataclass
class RunSummary:
    scraped: int = 0
    new: int = 0
    matched: int = 0
    notified: int = 0
    failed: list[str] = field(default_factory=list)


def run_once(scraper: Scraper, api_url: str, webhook_url: str, criteria: Criteria, store: SeenStore) -> RunSummary:
    summary = RunSummary()
    for flat in scraper.listings():
        summary.scraped += 1
        if flat.listing_id in store.ids:
            continue
        summary.new += 1
        enriched = Listing(**{**asdict(flat), "commute": commute_minutes(scraper.session, api_url, flat.listing_id)})
        if not criteria.matches(enriched):
            store.add(flat.listing_id)  # seen and rejected – don't re-check every run
            continue
        summary.matched += 1
        if notify(scraper.session, webhook_url, enriched):
            summary.notified += 1
            store.add(flat.listing_id)
        else:
            summary.failed.append(flat.listing_id)  # not marked seen → retried next run
    store.save()
    return summary


def schedule_bot(scheduler: schedule.Scheduler, minutes: int, job: Callable[[], RunSummary],
                 history: list[RunSummary]) -> schedule.Job:
    return scheduler.every(minutes).minutes.do(lambda: history.append(job())).tag("flat-hunter")


# --- a local fake website + API + webhook, for tests and the demo ----------------------------
FLATS = [
    {"id": "f1", "title": "Sunny 2-room in Alfama", "rent": 1150, "rooms": 2, "district": "alfama", "commute": 20},
    {"id": "f2", "title": "Loft near the river", "rent": 1700, "rooms": 1.5, "district": "belem", "commute": 35},
    {"id": "f3", "title": "Family flat, 3 rooms", "rent": 1300, "rooms": 3, "district": "alfama", "commute": 50},
    {"id": "f4", "title": "Cosy 2-room, Graça", "rent": 990, "rooms": 2, "district": "graca", "commute": 25},
    {"id": "f5", "title": "Studio with terrace", "rent": 800, "rooms": 1, "district": "graca", "commute": None},
]


class DemoSite:
    """``ThreadingHTTPServer`` on 127.0.0.1 with /robots.txt, /listings, /api/commute and /hook."""

    def __init__(self, per_page: int = 2, hook_failures: int = 0, disallow: str = "/admin") -> None:
        self.per_page, self.hook_failures, self.disallow = per_page, hook_failures, disallow
        self.received: list[dict[str, Any]] = []
        self.user_agents: set[str] = set()
        site = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args: object) -> None:  # keep test output clean
                pass

            def _send(self, status: int, body: str, kind: str = "text/html") -> None:
                data = body.encode()
                self.send_response(status)
                self.send_header("Content-Type", f"{kind}; charset=utf-8")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)

            def do_GET(self) -> None:  # noqa: N802 - http.server naming
                site.user_agents.add(self.headers.get("User-Agent", ""))
                url = urlparse(self.path)
                query = parse_qs(url.query)
                if url.path == "/robots.txt":
                    self._send(200, f"User-agent: *\nDisallow: {site.disallow}\n", "text/plain")
                elif url.path == "/listings":
                    self._send(200, site.page(int(query.get("page", ["1"])[0])))
                elif url.path == "/api/commute":
                    flat = next((f for f in FLATS if f["id"] == query.get("id", [""])[0]), None)
                    if flat is None or flat["commute"] is None:
                        self._send(404, '{"error": "unknown"}', "application/json")
                    else:
                        self._send(200, json.dumps({"minutes": flat["commute"]}), "application/json")
                else:
                    self._send(404, "not found")

            def do_POST(self) -> None:  # noqa: N802
                if self.path != "/hook":
                    self._send(404, "no such hook")
                    return
                body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
                if site.hook_failures > 0:
                    site.hook_failures -= 1
                    self._send(503, "busy")
                    return
                site.received.append(body)
                self._send(200, "ok", "text/plain")

        self.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.url = f"http://127.0.0.1:{self.server.server_address[1]}"

    def page(self, number: int) -> str:
        chunk = FLATS[(number - 1) * self.per_page: number * self.per_page]
        cards = "".join(
            f'<article class="listing" data-id="{f["id"]}" data-district="{f["district"]}">'
            f'<a href="/flat/{f["id"]}">{f["title"]}</a><span class="rent">€ {f["rent"]:,}</span>'
            f'<span class="rooms">{f["rooms"]} rooms</span></article>' for f in chunk)
        cards += '<article class="listing" data-id="ad"><p>Sponsored</p></article>'  # malformed card
        more = number * self.per_page < len(FLATS)
        nav = f'<a rel="next" href="/listings?page={number + 1}">next</a>' if more else ""
        return f"<html><body>{cards}{nav}</body></html>"

    def __enter__(self) -> DemoSite:
        threading.Thread(target=self.server.serve_forever, args=(0.05,), daemon=True).start()
        return self

    def __exit__(self, *exc: object) -> None:
        self.server.shutdown()
        self.server.server_close()


def main() -> None:
    print("Day 97 – Apartment-hunting bot\n")
    criteria = Criteria(max_rent=1400, min_rooms=2, max_commute=30)
    with DemoSite(hook_failures=1) as site, tempfile.TemporaryDirectory() as tmp:
        store = SeenStore(Path(tmp) / "seen.json")
        history: list[RunSummary] = []
        scheduler = schedule.Scheduler()

        def job() -> RunSummary:
            return run_once(Scraper(site.url), f"{site.url}/api", f"{site.url}/hook", criteria, store)

        print(schedule_bot(scheduler, 10, job, history))
        scheduler.run_all()  # first run
        scheduler.run_all()  # a later run: nothing new
        for n, summary in enumerate(history, 1):
            print(f"run {n}: {summary}")
        for message in site.received:
            print(message["text"].splitlines()[0])


if __name__ == "__main__":
    main()
