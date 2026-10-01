"""Day 29 – Using External Python Modules / Import.

Scenario: a *dependency inspector* for this course – it checks which
third-party packages are installed, reads their versions, uses one of them
(``requests``) offline, and organises its own helpers as a local package.

Deliverables (syllabus):
* ``import`` statements (``import x``, ``from x import y``, relative imports, lazy imports)
* Package installation (pip, checking what is installed and which version)
* Module organisation (a package with ``__init__.py`` and ``__all__``)
"""

from __future__ import annotations

import importlib
import importlib.util
import json  # standard library: always available
from importlib import metadata
from types import ModuleType

from packaging.requirements import Requirement  # third-party (installed with pip)
from packaging.version import Version

from . import toolkit  # relative import of our own package
from .toolkit.text import slug  # import one name from a submodule

DELIVERABLES: dict[str, str] = {
    "import statements (absolute, relative, from-import)": "toolkit",
    "lazy / optional imports": "optional_import",
    "checking installed packages": "is_installed",
    "reading package versions": "installed_version",
    "verifying requirements": "check_requirement",
    "using a third-party library": "build_query_url",
    "module organisation (package + __all__)": "toolkit",
}

INSTALL_HINT = "python -m pip install -r requirements.txt"


def is_installed(module_name: str) -> bool:
    """Look for a module without importing it (``find_spec``)."""
    return importlib.util.find_spec(module_name) is not None


def installed_version(distribution: str) -> str | None:
    """Version of a pip-installed distribution, or ``None`` when absent."""
    try:
        return metadata.version(distribution)
    except metadata.PackageNotFoundError:
        return None


def check_requirement(spec: str) -> tuple[bool, str]:
    """Check a requirement line such as ``"requests>=2.31"`` against what is installed."""
    requirement = Requirement(spec)
    version = installed_version(requirement.name)
    if version is None:
        return False, f"{requirement.name} missing – run: {INSTALL_HINT}"
    ok = requirement.specifier.contains(Version(version), prereleases=True)
    return ok, f"{requirement.name} {version} {'satisfies' if ok else 'does not satisfy'} {requirement.specifier or 'any'}"


def optional_import(module_name: str) -> ModuleType | None:
    """Import a module only if available – the pattern behind optional features."""
    try:
        return importlib.import_module(module_name)
    except ModuleNotFoundError:
        return None


def build_query_url(base: str, **params: str | int) -> str:
    """Use the third-party ``requests`` library offline to encode a URL safely."""
    requests = optional_import("requests")
    if requests is None:
        raise RuntimeError(f"requests is not installed – run: {INSTALL_HINT}")
    prepared = requests.Request("GET", base, params=params).prepare()
    return str(prepared.url)


def report(specs: list[str]) -> list[str]:
    lines = []
    for spec in specs:
        ok, message = check_requirement(spec)
        lines.append(f"{'✅' if ok else '❌'} {message}")
    return lines


def main() -> None:
    print("Day 29 – Dependency inspector\n")
    print("\n".join(report(["requests>=2.31", "pandas>=2.2", "not-a-real-package"])))
    print("\nOwn package API:", toolkit.__all__, "→", toolkit.slug("Day 29: Imports!"),
          toolkit.percent(29, 100))
    print("Same function via from-import:", slug("Hello World"))
    print("json is stdlib:", json.__name__, "| yaml optional:", optional_import("yaml") is not None)
    print("URL built by requests:", build_query_url("https://example.com/search", q="python imports", page=2))


if __name__ == "__main__":
    main()
