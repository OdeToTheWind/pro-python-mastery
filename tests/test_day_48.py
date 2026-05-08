# tests/test_day_48.py
import pytest

def test_tkinter_import():
    try:
        import tkinter
        assert tkinter is not None
    except ImportError:
        pytest.skip("Tkinter not available")