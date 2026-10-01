"""Day 14 – Code Blocks and Indentation.

Scenario: a *snippet linter for a coding bootcamp* – students paste code and
the tool compiles it, explains indentation errors and offers an automatic fix.

Deliverables (syllabus):
* Python indentation rules
* Loop and function blocks
* Common ``IndentationError`` fixes (and ``TabError``)
"""

from __future__ import annotations

from dataclasses import dataclass

DELIVERABLES: dict[str, str] = {
    "indentation rules (compile check)": "check_snippet",
    "loop and function blocks": "block_outline",
    "IndentationError / TabError fixes": "fix_tabs",
    "catalogue of common errors": "BROKEN_SNIPPETS",
}

BROKEN_SNIPPETS: dict[str, str] = {
    "expected an indented block": "def greet():\nprint('hi')\n",
    "unexpected indent": "x = 1\n    y = 2\n",
    "unindent does not match": "if True:\n        a = 1\n    b = 2\n",
    "mixed tabs and spaces": "if True:\n\tx = 1\n        y = 2\n",
}


@dataclass(frozen=True, slots=True)
class SnippetResult:
    ok: bool
    error: str | None = None
    line: int | None = None
    message: str = ""


def check_snippet(code: str) -> SnippetResult:
    """Compile *code* without running it and report indentation problems.

    ``TabError`` is a subclass of ``IndentationError``, which is a subclass of
    ``SyntaxError`` – so the most specific ``except`` must come first.
    """
    try:
        compile(code, "<snippet>", "exec")
    except TabError as exc:
        return SnippetResult(False, "TabError", exc.lineno, exc.msg)
    except IndentationError as exc:
        return SnippetResult(False, "IndentationError", exc.lineno, exc.msg)
    except SyntaxError as exc:
        return SnippetResult(False, "SyntaxError", exc.lineno, exc.msg)
    return SnippetResult(True)


def fix_tabs(code: str, width: int = 8) -> str:
    """Replace leading tabs with spaces – the fix for ``TabError``.

    The default of 8 matches how the Python tokenizer measures a tab, so the
    block structure the author intended is preserved.
    """
    fixed_lines = []
    for line in code.splitlines():
        stripped = line.lstrip(" \t")
        indent = line[: len(line) - len(stripped)].expandtabs(width)
        fixed_lines.append(indent + stripped)
    return "\n".join(fixed_lines) + ("\n" if code.endswith("\n") else "")


def indent_body(code: str, after_line: int, width: int = 4) -> str:
    """Indent every line after *after_line* – the fix for 'expected an indented block'."""
    lines = code.splitlines()
    for index in range(after_line, len(lines)):
        lines[index] = " " * width + lines[index]
    return "\n".join(lines) + "\n"


def block_outline(code: str) -> list[tuple[int, str]]:
    """List ``(depth, statement)`` pairs – shows how blocks nest under ``:`` lines."""
    outline: list[tuple[int, str]] = []
    for raw in code.expandtabs(4).splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        depth = (len(raw) - len(raw.lstrip(" "))) // 4
        outline.append((depth, raw.strip()))
    return outline


SAMPLE_PROGRAM = """\
def count_evens(numbers):
    total = 0
    for n in numbers:
        if n % 2 == 0:
            total += 1
    return total
"""


def main() -> None:
    print("Day 14 – Snippet linter\n")
    for label, code in BROKEN_SNIPPETS.items():
        result = check_snippet(code)
        print(f"{label:<28} → {result.error} on line {result.line}: {result.message}")
    print("\nAfter fixes:")
    print("  tabs fixed   →", check_snippet(fix_tabs(BROKEN_SNIPPETS["mixed tabs and spaces"])).ok)
    print("  body indented→", check_snippet(indent_body(BROKEN_SNIPPETS["expected an indented block"], 1)).ok)
    print("\nBlock outline of a correct program:")
    for depth, statement in block_outline(SAMPLE_PROGRAM):
        print(f"  {'│   ' * depth}{statement}")


if __name__ == "__main__":
    main()
