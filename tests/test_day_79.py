"""Tests for Day 79 – Packaging & Distribution (builds run offline in tmp_path)."""

import importlib.util
import subprocess
import sys
import tomllib
import zipfile

import pytest

from src.day_79_packaging_distribution.main import (
    BACKENDS,
    build_distributions,
    inspect_wheel,
    publish_commands,
    render_pyproject,
    scaffold,
    twine_check,
    validate_pyproject,
)

needs_build_tools = pytest.mark.skipif(
    not all(importlib.util.find_spec(m) for m in ("build", "hatchling", "twine")),
    reason="install requirements-dev.txt (build, hatchling, twine)",
)


@pytest.mark.parametrize("backend", sorted(BACKENDS))
def test_render_pyproject_is_valid_for_every_backend(backend):
    text = render_pyproject("kitchen-conv", "1.2.0rc1", backend)
    data = tomllib.loads(text)
    assert data["project"]["scripts"] == {"kitchen-conv": "kitchen_conv.cli:main"}
    assert data["build-system"]["build-backend"]
    assert validate_pyproject(text) == []


@pytest.mark.parametrize(
    ("name", "version", "backend"),
    [("Kitchen Conv", "1.0.0", "hatchling"), ("kc", "one", "hatchling"), ("kc", "1.0.0", "flit")],
)
def test_render_pyproject_rejects(name, version, backend):
    with pytest.raises(ValueError):
        render_pyproject(name, version, backend)


def test_validate_pyproject_reports_problems():
    assert validate_pyproject("not = [toml")[0].startswith("invalid TOML")
    problems = validate_pyproject('[project]\nname = "x"\nversion = "banana"\n')
    assert "missing [build-system].build-backend" in problems
    assert "missing [project].requires-python" in problems
    assert "version is not a valid release number" in problems


def test_scaffold_creates_src_layout(tmp_path):
    project = scaffold(tmp_path)
    assert (project / "src" / "kitchenconv" / "cli.py").exists()
    assert {p.name for p in project.iterdir()} == {"pyproject.toml", "README.md", "LICENSE", "src"}
    namespace = {}
    exec(compile((project / "src" / "kitchenconv" / "__init__.py").read_text(), "init", "exec"), namespace)  # noqa: S102
    assert namespace["convert"](2, "cup", "ml") == 480.0


@needs_build_tools
def test_build_inspect_check_and_install(tmp_path):
    project = scaffold(tmp_path, version="0.2.0")
    dists = build_distributions(project, tmp_path / "dist")
    assert [d.name for d in dists] == ["kitchenconv-0.2.0-py3-none-any.whl", "kitchenconv-0.2.0.tar.gz"]

    info = inspect_wheel(dists[0])
    assert (info["name"], info["version"], info["requires_python"]) == ("kitchenconv", "0.2.0", ">=3.12")
    assert info["tag"] == "py3-none-any"  # pure Python: one wheel for every OS
    assert "kitchenconv/cli.py" in info["files"]
    assert "kitchenconv = kitchenconv.cli:main" in info["entry_points"]

    ok, report = twine_check(dists)
    assert ok, report

    with zipfile.ZipFile(dists[0]) as wheel:  # install-free smoke test: import from the wheel
        wheel.extractall(tmp_path / "site")
    result = subprocess.run([sys.executable, "-c", "from kitchenconv.cli import main; main(['3', 'tbsp', 'tsp'])"],
                            capture_output=True, text=True, cwd=tmp_path / "site", check=True)
    assert result.stdout.strip() == "9.0"


def test_build_failure_is_reported(tmp_path):
    (tmp_path / "broken").mkdir()
    (tmp_path / "broken" / "pyproject.toml").write_text("[build-system]\nrequires=[]\nbuild-backend='nope.backend'\n")
    with pytest.raises(RuntimeError, match="build failed"):
        build_distributions(tmp_path / "broken", tmp_path / "dist")


def test_publish_commands_use_token_without_secrets():
    commands = publish_commands()
    assert "export TWINE_USERNAME=__token__" in commands
    assert any("--repository testpypi" in c for c in commands)
    assert all("pypi-AgE" not in c for c in commands)  # no real token ever embedded
