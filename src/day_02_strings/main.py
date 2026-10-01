"""Day 02 – String Manipulation.

Scenario: a *conference badge printer* that turns messy sign-up data into
clean, aligned badges.

Deliverables (syllabus):
* Advanced string methods
* Cleaning user input
* String formatting and alignment
"""

from __future__ import annotations

import re
import string

DELIVERABLES: dict[str, str] = {
    "advanced string methods": "make_handle",
    "cleaning input": "clean_name",
    "slug / normalisation": "slugify",
    "formatting and alignment": "render_badge",
    "tabular alignment": "align_columns",
}

BADGE_WIDTH = 32


def clean_name(raw: str) -> str:
    """Collapse whitespace and capitalise each word correctly.

    ``str.title()`` turns ``"o'neil"`` into ``"O'Neil"`` but ``"john's"`` into
    ``"John'S"``. ``string.capwords`` only capitalises after whitespace, and we
    additionally capitalise after hyphens for double-barrelled names.
    """
    collapsed = " ".join(raw.split())
    if not collapsed:
        raise ValueError("name cannot be empty")
    words = string.capwords(collapsed.lower())
    return "-".join(part[:1].upper() + part[1:] for part in words.split("-"))


def make_handle(name: str, years: int) -> str:
    """Create a social handle: first three letters + zero-padded experience."""
    if years < 0:
        raise ValueError("years cannot be negative")
    letters = "".join(ch for ch in name.casefold() if ch.isalpha())
    if not letters:
        raise ValueError("name must contain at least one letter")
    return f"@{letters[:3]}{years:02d}"


def slugify(text: str) -> str:
    """Turn arbitrary text into a URL-safe slug (``"Hello, World!" -> "hello-world"``)."""
    lowered = text.strip().casefold()
    return re.sub(r"[^a-z0-9]+", "-", lowered).strip("-")


def render_badge(raw_name: str, role: str, years: int) -> str:
    """Render a fixed-width badge using centring, padding and fill characters."""
    name = clean_name(raw_name)
    lines = [
        "=" * BADGE_WIDTH,
        f"{'PYCON BADGE':^{BADGE_WIDTH}}",
        "-" * BADGE_WIDTH,
        f"{name:^{BADGE_WIDTH}}",
        f"{role.strip().upper():^{BADGE_WIDTH}}",
        f"{make_handle(name, years):.^{BADGE_WIDTH}}",
        "=" * BADGE_WIDTH,
    ]
    return "\n".join(lines)


def align_columns(rows: list[tuple[str, str, float]]) -> list[str]:
    """Left-, centre- and right-align three columns of a sign-up table."""
    return [f"{name:<15}{city:^10}{fee:>8.2f}" for name, city, fee in rows]


def main() -> None:
    print("Day 02 – String Manipulation\n")
    print(render_badge("  ada   LOVELACE ", " senior engineer", 8))
    print(render_badge("mary-jane o'neil", "speaker", 3))
    print("\nSlug:", slugify("  Pro Python Mastery: Day 02!  "))
    for line in align_columns([("Ada Lovelace", "London", 49.5), ("Grace Hopper", "NYC", 120)]):
        print(line)


if __name__ == "__main__":
    main()
