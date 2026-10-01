"""Day 33 – Module Aliasing.

Scenario: a *fitness-tracker weekly summary* that needs two different
``loads`` functions and some long module names – aliasing keeps it readable.

Deliverables (syllabus):
* ``import module as alias``
* ``from module import name as alias`` (resolving name clashes)
* Code organisation and readability (conventional aliases, when *not* to alias)
"""

from __future__ import annotations

import datetime as dt  # conventional, short and unambiguous
import statistics as stats
from collections import Counter as Tally  # aliasing a class to a domain word
from json import loads as json_loads  # two different `loads` functions …
from tomllib import loads as toml_loads  # … would clash without aliases
from types import ModuleType

DELIVERABLES: dict[str, str] = {
    "import module as alias": "weekly_summary",
    "from module import name as alias": "load_settings",
    "resolving name clashes": "load_settings",
    "readability guidelines": "ALIAS_GUIDE",
    "inspecting what an alias refers to": "resolve_aliases",
}

ALIAS_GUIDE: dict[str, str] = {
    "import numpy as np": "community convention – everyone reads np instantly",
    "import pandas as pd": "community convention",
    "import datetime as dt": "avoids datetime.datetime stutter",
    "from json import loads as json_loads": "resolves a clash with tomllib.loads",
    "import math as m": "avoid – single letters hide meaning (see Day 04)",
}


def resolve_aliases() -> dict[str, str]:
    """Show the real module/object behind each alias used in this file."""
    aliases: dict[str, object] = {"dt": dt, "stats": stats, "Tally": Tally,
                                  "json_loads": json_loads, "toml_loads": toml_loads}
    resolved = {}
    for alias, target in aliases.items():
        if isinstance(target, ModuleType):
            resolved[alias] = target.__name__
        else:
            resolved[alias] = f"{getattr(target, '__module__', '?')}.{getattr(target, '__qualname__', '?')}"
    return resolved


def load_settings(json_text: str, toml_text: str) -> dict[str, object]:
    """Merge JSON (from the watch) and TOML (user config) – both called ``loads``."""
    return {**json_loads(json_text), **toml_loads(toml_text)}


def weekly_summary(steps_by_day: dict[str, int], week_start: dt.date) -> dict[str, object]:
    values = list(steps_by_day.values())
    if not values:
        raise ValueError("no data for this week")
    week_end = week_start + dt.timedelta(days=6)
    activity = Tally("active" if v >= 8000 else "rest" for v in values)
    return {
        "range": f"{week_start:%d %b} – {week_end:%d %b}",
        "mean": round(stats.mean(values)),
        "median": stats.median(values),
        "best_day": max(steps_by_day, key=steps_by_day.__getitem__),
        "active_days": activity["active"],
    }


def main() -> None:
    print("Day 33 – Fitness summary with aliases\n")
    week = {"Mon": 9120, "Tue": 4300, "Wed": 11050, "Thu": 7600, "Fri": 8800}
    print(weekly_summary(week, dt.date(2026, 4, 13)))
    print(load_settings('{"device": "watch", "goal": 8000}', 'goal = 10000\nunits = "metric"'))
    print("\nWhat the aliases really are:")
    for alias, target in resolve_aliases().items():
        print(f"  {alias:<11} → {target}")


if __name__ == "__main__":
    main()
