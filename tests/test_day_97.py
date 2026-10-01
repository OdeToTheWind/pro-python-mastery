"""Tests for Day 97 – Automation Bot Suite (local HTTP server, no internet)."""

import json

import pytest
import requests
import schedule

from src.day_97_automation_bot_suite.main import (
    USER_AGENT,
    Criteria,
    DemoSite,
    Listing,
    RunSummary,
    Scraper,
    SeenStore,
    commute_minutes,
    main,
    notify,
    run_once,
    schedule_bot,
)

CRITERIA = Criteria(max_rent=1400, min_rooms=2, max_commute=30)


@pytest.fixture
def site():
    with DemoSite() as demo:
        yield demo


def test_scraper_follows_pages_and_skips_bad_cards(site):
    flats = list(Scraper(site.url).listings())
    assert [f.listing_id for f in flats] == ["f1", "f2", "f3", "f4", "f5"]
    assert flats[1] == Listing("f2", "Loft near the river", 1700, 1.5, "belem", f"{site.url}/flat/f2")
    assert site.user_agents == {USER_AGENT}
    assert len(list(Scraper(site.url, max_pages=1).listings())) == 2


def test_robots_txt_is_respected():
    with DemoSite(disallow="/listings") as blocked:
        scraper = Scraper(blocked.url)
        with pytest.raises(PermissionError, match="robots.txt"):
            next(scraper.listings())
        assert scraper.allowed("/about")
    offline = Scraper("http://127.0.0.1:9", timeout=0.2)
    assert offline.allowed("/listings?page=1")  # unreachable robots.txt = no rules


def test_commute_api(site):
    session = requests.Session()
    assert commute_minutes(session, f"{site.url}/api", "f1") == 20
    assert commute_minutes(session, f"{site.url}/api", "f5") is None  # 404
    assert commute_minutes(session, "http://127.0.0.1:9", "f1", timeout=0.2) is None


@pytest.mark.parametrize(
    ("flat", "expected"),
    [(Listing("a", "t", 1000, 2, "graca", "u", 20), True),
     (Listing("a", "t", 1500, 2, "graca", "u", 20), False),
     (Listing("a", "t", 1000, 1, "graca", "u", 20), False),
     (Listing("a", "t", 1000, 2, "graca", "u", 31), False),
     (Listing("a", "t", 1000, 2, "graca", "u", None), False)],
)
def test_criteria(flat, expected):
    assert CRITERIA.matches(flat) is expected
    assert Criteria(2000, districts=frozenset({"belem"})).matches(flat) is False


def test_seen_store_persists_atomically(tmp_path):
    store = SeenStore(tmp_path / "state" / "seen.json")
    store.add("b")
    store.add("a")
    store.save()
    assert json.loads((tmp_path / "state" / "seen.json").read_text()) == ["a", "b"]
    assert SeenStore(tmp_path / "state" / "seen.json").ids == {"a", "b"}
    assert [p.name for p in (tmp_path / "state").iterdir()] == ["seen.json"]


def test_notify_retries_server_errors_but_not_client_errors():
    flat = Listing("f1", "Flat", 900, 2, "x", "http://u", 10)
    with DemoSite(hook_failures=2) as flaky:
        assert notify(requests.Session(), f"{flaky.url}/hook", flat, retries=2)
        assert flaky.received[0]["listing"]["listing_id"] == "f1"
        assert "€900, 2 rooms, 10 min commute" in flaky.received[0]["text"]
    with DemoSite(hook_failures=5) as down:
        assert not notify(requests.Session(), f"{down.url}/hook", flat, retries=1)
    with DemoSite() as site:
        assert not notify(requests.Session(), f"{site.url}/nowhere", flat)  # 404 is final
    assert not notify(requests.Session(), "http://127.0.0.1:9/hook", flat, retries=0, timeout=0.2)


def test_run_once_dedupes_across_runs(tmp_path):
    with DemoSite(hook_failures=1) as site:
        def run():
            store = SeenStore(tmp_path / "seen.json")
            return run_once(Scraper(site.url), f"{site.url}/api", f"{site.url}/hook", CRITERIA, store)

        first, second, third = run(), run(), run()
    assert (first.scraped, first.new, first.matched, first.notified) == (5, 5, 2, 2)
    assert (second.new, third.new) == (0, 0)
    assert sorted(m["listing"]["listing_id"] for m in site.received) == ["f1", "f4"]


def test_failed_notification_is_retried_next_run(tmp_path):
    with DemoSite(hook_failures=3) as site:
        store = SeenStore(tmp_path / "seen.json")
        args = (Scraper(site.url), f"{site.url}/api", f"{site.url}/hook", CRITERIA, store)
        first = run_once(*args)
        second = run_once(*args)
    assert first.failed == ["f1"] and first.notified == 1
    assert second.new == 1 and second.notified == 1


def test_schedule_bot_registers_job():
    scheduler, history = schedule.Scheduler(), []
    job = schedule_bot(scheduler, 15, lambda: RunSummary(scraped=1), history)
    assert job.interval == 15 and job.unit == "minutes" and "flat-hunter" in job.tags
    scheduler.run_all()
    assert history == [RunSummary(scraped=1)]


def test_main(capsys):
    main()
    out = capsys.readouterr().out
    assert "run 1: RunSummary(scraped=5, new=5, matched=2, notified=2" in out and "Cosy 2-room" in out
