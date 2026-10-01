"""Tests for Day 55 – Date and Time."""

from datetime import UTC, date, datetime, time, timedelta

import pytest

from src.day_55_date_and_time.main import (
    add_business_days,
    age_on,
    humanize_delta,
    main,
    meeting_in_zones,
    now_utc,
    parse_date,
    utc_offset_hours,
)


def test_now_utc_is_aware():
    assert now_utc().tzinfo is UTC


@pytest.mark.parametrize("text", ["2026-05-06", "06/05/2026", "6 May 2026", "May 06, 2026", " 2026-05-06 "])
def test_parse_date_formats(text):
    assert parse_date(text) == date(2026, 5, 6)


def test_parse_date_rejects():
    with pytest.raises(ValueError, match="YYYY-MM-DD"):
        parse_date("next Tuesday")


@pytest.mark.parametrize(
    ("birth", "today", "age"),
    [
        (date(2000, 5, 7), date(2026, 5, 6), 25),  # day before birthday
        (date(2000, 5, 6), date(2026, 5, 6), 26),  # on the birthday
        (date(2000, 2, 29), date(2026, 2, 28), 25),  # leap-day birthday
        (date(2000, 2, 29), date(2026, 3, 1), 26),
    ],
)
def test_age_on(birth, today, age):
    assert age_on(birth, today) == age


def test_age_in_future():
    with pytest.raises(ValueError):
        age_on(date(2030, 1, 1), date(2026, 1, 1))


def test_add_business_days_skips_weekends_and_holidays():
    friday = date(2026, 5, 8)
    assert add_business_days(friday, 1) == date(2026, 5, 11)
    assert add_business_days(friday, 1, {date(2026, 5, 11)}) == date(2026, 5, 12)
    assert add_business_days(friday, 0) == friday
    with pytest.raises(ValueError):
        add_business_days(friday, -1)


@pytest.mark.parametrize(
    ("delta", "text"),
    [(timedelta(days=3, hours=8, minutes=30), "in 3 days 8 hours"),
     (timedelta(hours=1, minutes=1), "in 1 hour 1 minute"),
     (timedelta(minutes=-90), "1 hour 30 minutes ago"),
     (timedelta(seconds=20), "in less than a minute")],
)
def test_humanize_delta(delta, text):
    assert humanize_delta(delta) == text


def test_meeting_in_zones_converts_correctly():
    zones = meeting_in_zones(date(2026, 5, 12), time(15, 0), "Europe/Berlin")
    assert zones["Lukas"] == "Tue 12 May 15:00 CEST"
    assert zones["Asha"] == "Tue 12 May 18:30 IST"
    assert zones["Ken"] == "Tue 12 May 22:00 JST"
    assert zones["Maria"].startswith("Tue 12 May 10:00")


def test_dst_changes_offset():
    assert utc_offset_hours("Europe/Berlin", datetime(2026, 1, 15, tzinfo=UTC)) == 1
    assert utc_offset_hours("Europe/Berlin", datetime(2026, 7, 15, tzinfo=UTC)) == 2
    assert utc_offset_hours("Asia/Kolkata", datetime(2026, 7, 15, tzinfo=UTC)) == 5.5


def test_main(capsys):
    main()
    out = capsys.readouterr().out
    assert "Deadline in 3 days 8 hours" in out
    assert "(DST): 1.0 2.0" in out
