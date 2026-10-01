"""Day 55 – Working with Date and Time.

Scenario: a *global team meeting planner* – ages, deadlines, business days and
one meeting shown in every teammate's local time.

Deliverables (syllabus):
* ``datetime`` usage (``date``, ``datetime``, ``timedelta``)
* Calculations (exact age, business days, countdowns)
* Formatting and parsing (``strftime`` / ``strptime`` / ISO 8601)
* Timezone awareness (``zoneinfo``, UTC storage, DST transitions)
"""

from __future__ import annotations

from datetime import UTC, date, datetime, time, timedelta
from zoneinfo import ZoneInfo

DELIVERABLES: dict[str, str] = {
    "exact age calculation": "age_on",
    "business-day arithmetic": "add_business_days",
    "parsing several formats": "parse_date",
    "formatting": "humanize_delta",
    "timezone-aware conversion": "meeting_in_zones",
    "DST awareness": "utc_offset_hours",
    "aware 'now' in UTC": "now_utc",
}

TEAM = {"Asha": "Asia/Kolkata", "Lukas": "Europe/Berlin", "Maria": "America/Sao_Paulo",
        "Ken": "Asia/Tokyo"}
FORMATS = ("%Y-%m-%d", "%d/%m/%Y", "%d %b %Y", "%B %d, %Y")


def now_utc() -> datetime:
    """Store and compare times in UTC; ``datetime.now()`` without tz is naive."""
    return datetime.now(UTC)


def parse_date(text: str) -> date:
    for fmt in FORMATS:
        try:
            return datetime.strptime(text.strip(), fmt).date()
        except ValueError:
            continue
    raise ValueError(f"unrecognised date {text!r}; try YYYY-MM-DD")


def age_on(birth: date, today: date) -> int:
    """Exact age: subtract one if this year's birthday hasn't happened yet.

    ``days // 365`` is wrong around birthdays because of leap years.
    """
    if birth > today:
        raise ValueError("birth date is in the future")
    had_birthday = (today.month, today.day) >= (birth.month, birth.day)
    return today.year - birth.year - (0 if had_birthday else 1)


def add_business_days(start: date, days: int, holidays: set[date] | None = None) -> date:
    """Move forward *days* working days, skipping weekends and holidays."""
    if days < 0:
        raise ValueError("days must be non-negative")
    holidays = holidays or set()
    current = start
    while days:
        current += timedelta(days=1)
        if current.weekday() < 5 and current not in holidays:
            days -= 1
    return current


def humanize_delta(delta: timedelta) -> str:
    sign = "in " if delta >= timedelta(0) else ""
    suffix = "" if delta >= timedelta(0) else " ago"
    seconds = abs(int(delta.total_seconds()))
    days, rem = divmod(seconds, 86_400)
    hours, rem = divmod(rem, 3_600)
    minutes = rem // 60
    parts = [f"{v} {unit}{'s' if v != 1 else ''}" for v, unit in
             ((days, "day"), (hours, "hour"), (minutes, "minute")) if v]
    return f"{sign}{' '.join(parts[:2]) or 'less than a minute'}{suffix}"


def meeting_in_zones(local_day: date, local_time: time, organizer_tz: str,
                     team: dict[str, str] = TEAM) -> dict[str, str]:
    """Create an *aware* datetime in the organiser's zone and convert it for everyone."""
    start = datetime.combine(local_day, local_time, tzinfo=ZoneInfo(organizer_tz))
    return {name: start.astimezone(ZoneInfo(tz)).strftime("%a %d %b %H:%M %Z") for name, tz in team.items()}


def utc_offset_hours(zone: str, moment: datetime) -> float:
    offset = moment.astimezone(ZoneInfo(zone)).utcoffset() or timedelta(0)
    return offset.total_seconds() / 3600


def main() -> None:
    today = date(2026, 5, 6)
    print("Day 55 – Global team planner\n")
    print("Parsed:", [parse_date(t).isoformat() for t in ("2026-05-06", "06/05/2026", "6 May 2026")])
    print("Age on", today, "for 2000-05-07:", age_on(date(2000, 5, 7), today))
    print("5 business days after Fri 8 May:", add_business_days(date(2026, 5, 8), 5))
    deadline = datetime(2026, 5, 9, 18, tzinfo=UTC)
    print("Deadline", humanize_delta(deadline - datetime(2026, 5, 6, 9, 30, tzinfo=UTC)))
    for name, local in meeting_in_zones(date(2026, 5, 12), time(15, 0), "Europe/Berlin").items():
        print(f"  {name:<6} {local}")
    march, may = datetime(2026, 3, 1, tzinfo=UTC), datetime(2026, 5, 1, tzinfo=UTC)
    print("Berlin UTC offset Mar vs May (DST):", utc_offset_hours("Europe/Berlin", march),
          utc_offset_hours("Europe/Berlin", may))


if __name__ == "__main__":
    main()
