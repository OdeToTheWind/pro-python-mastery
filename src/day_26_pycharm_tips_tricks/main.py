"""Day 26 – PyCharm Tips and Tricks.

Scenario: a *pocket IDE coach* – a searchable shortcut cheat-sheet per OS, a
live-template expander and a safe "Rename" refactoring that works the way the
IDE's does (on tokens, not on raw text).

Deliverables (syllabus):
* IDE productivity (shortcut lookup per OS)
* Debugging tools (debugger shortcuts and features)
* Refactoring tools (token-aware rename)
* Templates (live-template expansion)
* Shortcuts
"""

from __future__ import annotations

import io
import keyword
import tokenize
from dataclasses import dataclass

DELIVERABLES: dict[str, str] = {
    "IDE productivity / shortcuts": "find_shortcuts",
    "debugging tools": "SHORTCUTS",
    "refactoring tools (Rename)": "safe_rename",
    "live templates": "expand_template",
    "cheat sheet": "cheat_sheet",
}


@dataclass(frozen=True, slots=True)
class Shortcut:
    action: str
    category: str
    windows_linux: str
    macos: str


SHORTCUTS: tuple[Shortcut, ...] = (
    Shortcut("Search everywhere", "navigation", "Shift Shift", "⇧ ⇧"),
    Shortcut("Go to declaration", "navigation", "Ctrl+B", "⌘B"),
    Shortcut("Recent files", "navigation", "Ctrl+E", "⌘E"),
    Shortcut("Rename", "refactoring", "Shift+F6", "⇧F6"),
    Shortcut("Extract method", "refactoring", "Ctrl+Alt+M", "⌥⌘M"),
    Shortcut("Extract variable", "refactoring", "Ctrl+Alt+V", "⌥⌘V"),
    Shortcut("Reformat code", "editing", "Ctrl+Alt+L", "⌥⌘L"),
    Shortcut("Show intention actions", "editing", "Alt+Enter", "⌥↩"),
    Shortcut("Toggle breakpoint", "debugging", "Ctrl+F8", "⌘F8"),
    Shortcut("Debug current file", "debugging", "Shift+F9", "⌃D"),
    Shortcut("Step over", "debugging", "F8", "F8"),
    Shortcut("Step into", "debugging", "F7", "F7"),
    Shortcut("Evaluate expression", "debugging", "Alt+F8", "⌥F8"),
    Shortcut("Run current file", "running", "Ctrl+Shift+F10", "⌃⇧R"),
)

LIVE_TEMPLATES: dict[str, str] = {
    "main": 'if __name__ == "__main__":\n    $END$',
    "iter": "for $VAR$ in $ITERABLE$:\n    $END$",
    "prop": "@property\ndef $NAME$(self):\n    return self._$NAME$",
    "test": "def test_$NAME$():\n    assert $END$",
}


def find_shortcuts(query: str, os_name: str = "windows") -> list[str]:
    """Case-insensitive search over action names and categories."""
    key = "macos" if os_name.lower() in {"mac", "macos", "darwin"} else "windows_linux"
    q = query.lower()
    return [
        f"{s.action}: {getattr(s, key)}"
        for s in SHORTCUTS
        if q in s.action.lower() or q == s.category
    ]


def expand_template(abbreviation: str, **variables: str) -> str:
    """Expand a live template; unfilled variables keep their ``$NAME$`` marker."""
    if abbreviation not in LIVE_TEMPLATES:
        raise KeyError(f"no live template {abbreviation!r}")
    body = LIVE_TEMPLATES[abbreviation]
    for name, value in variables.items():
        body = body.replace(f"${name.upper()}$", value)
    return body.replace("$END$", variables.get("end", "pass"))


def safe_rename(source: str, old: str, new: str) -> str:
    """Rename an identifier like the IDE does: only NAME tokens change.

    A text search-and-replace would also change ``old`` inside strings,
    comments and longer names such as ``old_total``.
    """
    if not new.isidentifier() or keyword.iskeyword(new):
        raise ValueError(f"{new!r} is not a valid identifier")
    tokens = []
    for tok in tokenize.generate_tokens(io.StringIO(source).readline):
        if tok.type == tokenize.NAME and tok.string == old:
            tok = tok._replace(string=new)
        tokens.append(tok)
    return tokenize.untokenize(tokens)


def cheat_sheet(os_name: str = "windows") -> str:
    """Grouped, numbered cheat sheet (numbering added once, by enumerate)."""
    key = "macos" if os_name == "macos" else "windows_linux"
    lines: list[str] = []
    for category in dict.fromkeys(s.category for s in SHORTCUTS):
        lines.append(category.upper())
        group = [s for s in SHORTCUTS if s.category == category]
        for number, shortcut in enumerate(group, start=1):
            lines.append(f"  {number}. {shortcut.action:<24}{getattr(shortcut, key)}")
    return "\n".join(lines)


def main() -> None:
    print("Day 26 – Pocket IDE coach\n")
    print(cheat_sheet())
    print("\nSearch 'debugging' on macOS:", find_shortcuts("debugging", "macos"))
    print("\nLive template 'iter':\n" + expand_template("iter", var="user", iterable="users", end="print(user)"))
    code = "total = 1\nsubtotal = total + 1  # total\nprint('total', total)\n"
    print("\nSafe rename total → amount:\n" + safe_rename(code, "total", "amount"))


if __name__ == "__main__":
    main()
