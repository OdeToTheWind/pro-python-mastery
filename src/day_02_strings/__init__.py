# src/day_02_strings/__init__.py

# This allows someone to use: from src.day_02_strings import generate_profile
# rather than: from src.day_02_strings.main import generate_profile
from .main import generate_profile, run_string_demonstration

__all__ = ["generate_profile", "run_string_demonstration"]