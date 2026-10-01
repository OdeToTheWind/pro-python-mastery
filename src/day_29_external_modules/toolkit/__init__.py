"""A tiny local package used to teach module organisation on Day 29.

``__init__.py`` turns the folder into a package and chooses the public API:
``from toolkit import slug, percent`` works because of the re-exports below.
"""

from .formatting import percent
from .text import slug

__all__ = ["percent", "slug"]
