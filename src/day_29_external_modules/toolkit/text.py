"""Text helpers (one responsibility per module)."""

import re


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.casefold()).strip("-")
