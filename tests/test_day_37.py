# tests/test_day_37.py
import pytest

def test_turtle_import():
    """Skip gracefully if Tkinter is not available"""
    try:
        import turtle
        assert turtle is not None
        assert hasattr(turtle, "Turtle")
    except (ImportError, ModuleNotFoundError):
        pytest.skip("Tkinter/_tkinter not available in this environment")