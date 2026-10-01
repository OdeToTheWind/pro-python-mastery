"""Day 79 – Packaging & Distribution.

Scenario: publish *"kitchenconv"*, a tiny cooking-unit converter with a CLI,
as a real Python package: generate a ``src``-layout project with a complete
``pyproject.toml``, build a wheel and an sdist offline, inspect what is inside,
validate the metadata with ``twine check`` and prepare (not perform) the
TestPyPI upload.

Deliverables (syllabus):
* ``pyproject.toml`` (PEP 621 metadata, dependencies, scripts, optional extras)
* Build backends: setuptools, hatch(ling) and poetry – the same project three ways
* Wheels (and sdists): building and inspecting them
* Test publishing to PyPI (TestPyPI commands, API tokens, ``twine check``)
"""

from __future__ import annotations

import re
import subprocess
import sys
import tomllib
import zipfile
from pathlib import Path

DELIVERABLES: dict[str, str] = {
    "pyproject.toml generation": "render_pyproject",
    "pyproject.toml validation": "validate_pyproject",
    "build backends compared": "BACKENDS",
    "src-layout project scaffold": "scaffold",
    "building wheel + sdist": "build_distributions",
    "inspecting a wheel": "inspect_wheel",
    "twine check": "twine_check",
    "TestPyPI publishing steps": "publish_commands",
}

NAME_RE = re.compile(r"^[a-z0-9]+([._-][a-z0-9]+)*$")
VERSION_RE = re.compile(r"^\d+\.\d+\.\d+([ab]|rc)?\d*$")

BACKENDS: dict[str, str] = {
    "hatchling": '[build-system]\nrequires = ["hatchling>=1.25"]\nbuild-backend = "hatchling.build"\n',
    "setuptools": '[build-system]\nrequires = ["setuptools>=69", "wheel"]\nbuild-backend = "setuptools.build_meta"\n'
                  '\n[tool.setuptools.packages.find]\nwhere = ["src"]\n',
    "poetry": '[build-system]\nrequires = ["poetry-core>=1.9"]\nbuild-backend = "poetry.core.masonry.api"\n'
              '# Poetry ≥ 2 reads the standard [project] table too.\n',
}

PACKAGE_INIT = '''"""Convert cooking units."""

__version__ = "{version}"

ML_PER = {{"cup": 240.0, "tbsp": 15.0, "tsp": 5.0, "ml": 1.0}}


def convert(amount: float, from_unit: str, to_unit: str) -> float:
    return round(amount * ML_PER[from_unit] / ML_PER[to_unit], 2)
'''

PACKAGE_CLI = '''import argparse

from kitchenconv import __version__, convert


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="kitchenconv")
    parser.add_argument("amount", type=float)
    parser.add_argument("from_unit")
    parser.add_argument("to_unit")
    parser.add_argument("--version", action="version", version=__version__)
    args = parser.parse_args(argv)
    print(convert(args.amount, args.from_unit, args.to_unit))
    return 0
'''


def render_pyproject(name: str, version: str, backend: str = "hatchling") -> str:
    """A complete PEP 621 ``pyproject.toml`` for the chosen build backend."""
    if not NAME_RE.match(name):
        raise ValueError("package names: lowercase letters, digits, '.', '_' or '-'")
    if not VERSION_RE.match(version):
        raise ValueError("version must look like 1.2.3 (optionally a1, b2, rc1)")
    if backend not in BACKENDS:
        raise ValueError(f"backend must be one of {sorted(BACKENDS)}")
    module = name.replace("-", "_")
    return f'''{BACKENDS[backend]}
[project]
name = "{name}"
version = "{version}"
description = "Convert cooking units from the command line"
readme = "README.md"
requires-python = ">=3.12"
license = "MIT"
authors = [{{ name = "Pro Python Mastery learner" }}]
keywords = ["cooking", "units", "converter"]
classifiers = [
    "Programming Language :: Python :: 3",
    "Operating System :: OS Independent",
]
dependencies = []

[project.optional-dependencies]
dev = ["pytest>=8"]

[project.scripts]
{name} = "{module}.cli:main"

[project.urls]
Homepage = "https://github.com/OdeToTheWind/pro-python-mastery"
'''


def validate_pyproject(text: str) -> list[str]:
    """Return a list of problems (empty means OK)."""
    try:
        data = tomllib.loads(text)
    except tomllib.TOMLDecodeError as exc:
        return [f"invalid TOML: {exc}"]
    problems = []
    if "build-backend" not in data.get("build-system", {}):
        problems.append("missing [build-system].build-backend")
    project = data.get("project", {})
    for key in ("name", "version", "requires-python", "readme"):
        if key not in project:
            problems.append(f"missing [project].{key}")
    if "version" in project and not VERSION_RE.match(str(project["version"])):
        problems.append("version is not a valid release number")
    return problems


def scaffold(root: Path, name: str = "kitchenconv", version: str = "0.1.0", backend: str = "hatchling") -> Path:
    """Create a minimal, publishable src-layout project and return its folder."""
    project = root / name
    package = project / "src" / name.replace("-", "_")
    package.mkdir(parents=True)
    (project / "pyproject.toml").write_text(render_pyproject(name, version, backend), encoding="utf-8")
    (project / "README.md").write_text(f"# {name}\n\n`{name} 2 cup ml` → 480.0\n", encoding="utf-8")
    (project / "LICENSE").write_text("MIT License\n", encoding="utf-8")
    (package / "__init__.py").write_text(PACKAGE_INIT.format(version=version), encoding="utf-8")
    (package / "cli.py").write_text(PACKAGE_CLI, encoding="utf-8")
    return project


def build_distributions(project: Path, out_dir: Path) -> list[Path]:
    """``python -m build`` creates the sdist and the wheel. ``--no-isolation`` uses the
    already-installed backend, so this works offline (CI/classrooms)."""
    result = subprocess.run(
        [sys.executable, "-m", "build", "--no-isolation", "--outdir", str(out_dir), str(project)],
        capture_output=True, text=True, check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"build failed:\n{result.stdout}\n{result.stderr}")
    return sorted(out_dir.iterdir())


def inspect_wheel(wheel: Path) -> dict[str, object]:
    """A wheel is a zip file with the code plus ``*.dist-info`` metadata."""
    with zipfile.ZipFile(wheel) as archive:
        names = archive.namelist()
        meta_name = next(n for n in names if n.endswith(".dist-info/METADATA"))
        metadata = archive.read(meta_name).decode("utf-8")
        entry_name = next((n for n in names if n.endswith(".dist-info/entry_points.txt")), None)
        entry_points = archive.read(entry_name).decode("utf-8") if entry_name else ""
    fields = dict(line.split(": ", 1) for line in metadata.splitlines() if ": " in line and not line.startswith(" "))
    return {"files": sorted(n for n in names if not n.endswith("/")), "name": fields.get("Name"),
            "version": fields.get("Version"), "requires_python": fields.get("Requires-Python"),
            "entry_points": entry_points.strip(),
            "tag": wheel.name.removesuffix(".whl").split("-", 2)[2]}


def twine_check(dist_files: list[Path]) -> tuple[bool, str]:
    """Validate metadata/README rendering offline before uploading anywhere."""
    result = subprocess.run([sys.executable, "-m", "twine", "check", *map(str, dist_files)],
                            capture_output=True, text=True, check=False)
    return result.returncode == 0, result.stdout + result.stderr


def publish_commands(dist_dir: str = "dist") -> list[str]:
    """The TestPyPI rehearsal – printed for the learner, never executed here."""
    return [
        "# 1. create an account on https://test.pypi.org and an API token (scope: this project)",
        "# 2. never put the token in the repo: export it or use a CI secret",
        "export TWINE_USERNAME=__token__",
        "export TWINE_PASSWORD=pypi-<your-test-pypi-token>",
        f"python -m twine upload --repository testpypi {dist_dir}/*",
        "python -m pip install --index-url https://test.pypi.org/simple/ --no-deps kitchenconv",
        "# 3. when it works, tag a release and publish to real PyPI (prefer GitHub 'trusted publishing')",
    ]


def main() -> None:
    import tempfile

    print("Day 79 – Packaging kitchenconv\n")
    with tempfile.TemporaryDirectory() as tmp:
        project = scaffold(Path(tmp))
        print("pyproject problems:", validate_pyproject((project / "pyproject.toml").read_text()) or "none")
        try:
            dists = build_distributions(project, Path(tmp) / "dist")
        except RuntimeError as exc:
            print("could not build here (install requirements-dev.txt):", str(exc).splitlines()[0])
            return
        print("built:", [d.name for d in dists])
        wheel = next(d for d in dists if d.suffix == ".whl")
        info = inspect_wheel(wheel)
        print("wheel tag:", info["tag"], "| entry points:", str(info["entry_points"]).replace("\n", " "))
        print("twine check passed:", twine_check(dists)[0])
    print("\nTestPyPI rehearsal:\n  " + "\n  ".join(publish_commands()))


if __name__ == "__main__":
    main()
