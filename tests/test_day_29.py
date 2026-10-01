"""Tests for Day 29 – External Modules / Import."""

import pytest

from src.day_29_external_modules import main as day29
from src.day_29_external_modules import toolkit
from src.day_29_external_modules.main import (
    build_query_url,
    check_requirement,
    installed_version,
    is_installed,
    optional_import,
    report,
)


def test_is_installed():
    assert is_installed("json")
    assert is_installed("requests")
    assert not is_installed("definitely_not_a_module_xyz")


def test_installed_version():
    assert installed_version("requests").count(".") >= 1
    assert installed_version("definitely-not-a-dist-xyz") is None


@pytest.mark.parametrize(
    ("spec", "ok"),
    [("requests>=2.0", True), ("requests<1.0", False), ("missing-dist-xyz", False)],
)
def test_check_requirement(spec, ok):
    assert check_requirement(spec)[0] is ok


def test_missing_requirement_suggests_pip():
    assert "pip install" in check_requirement("missing-dist-xyz")[1]


def test_optional_import():
    assert optional_import("json").__name__ == "json"
    assert optional_import("missing_module_xyz") is None


def test_build_query_url_encodes_with_requests():
    assert build_query_url("https://x.org/s", q="a b&c", page=2) == "https://x.org/s?q=a+b%26c&page=2"


def test_build_query_url_without_requests(monkeypatch):
    monkeypatch.setattr(day29, "optional_import", lambda _name: None)
    with pytest.raises(RuntimeError, match="pip install"):
        build_query_url("https://x.org")


def test_package_public_api():
    assert toolkit.__all__ == ["percent", "slug"]
    assert toolkit.slug("Hello, World") == "hello-world"
    assert toolkit.percent(1, 3) == "33.3%"
    assert toolkit.percent(1, 0) == "n/a"


def test_report():
    lines = report(["requests>=2.0", "missing-dist-xyz"])
    assert lines[0].startswith("✅") and lines[1].startswith("❌")


def test_main(capsys):
    day29.main()
    assert "q=python+imports&page=2" in capsys.readouterr().out
