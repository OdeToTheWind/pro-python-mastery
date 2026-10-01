"""Day 41 – File I/O: Reading and Writing Local Files.

Scenario: a *daily journal* stored as a UTF-8 text file – one entry per line.

Deliverables (syllabus):
* ``open()`` with explicit modes and encodings
* ``with`` statements (files always closed)
* File-handling patterns: overwrite vs append, line-by-line streaming,
  EAFP error handling, atomic writes that never leave a half-written file
"""

from __future__ import annotations

import os
import tempfile
from collections.abc import Iterator
from datetime import date
from pathlib import Path

DELIVERABLES: dict[str, str] = {
    "open() modes w / a / r / x": "write_entries",
    "with statement": "append_entry",
    "streaming line by line": "iter_entries",
    "EAFP: reading a file that may not exist": "read_entries",
    "atomic write (temp file + replace)": "atomic_write",
    "exclusive create (mode 'x')": "create_new",
    "default data location": "default_journal_path",
}

ENCODING = "utf-8"


def default_journal_path() -> Path:
    """Demo data goes in ``.data/`` (git-ignored), never in the source tree."""
    return Path.cwd() / ".data" / "journal.txt"


def _line(entry: str) -> str:
    text = " ".join(entry.split())
    if not text:
        raise ValueError("entry cannot be empty")
    return text + "\n"  # every line ends with a newline, so appends never glue lines together


def write_entries(path: Path, entries: list[str]) -> int:
    """Overwrite the journal (mode ``"w"``). Returns the number of lines written."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding=ENCODING) as handle:
        handle.writelines(_line(e) for e in entries)
    return len(entries)


def append_entry(path: Path, entry: str, day: date | None = None) -> None:
    """Add one dated line (mode ``"a"``) – the file is created if missing."""
    if not entry.strip():
        raise ValueError("entry cannot be empty")
    path.parent.mkdir(parents=True, exist_ok=True)
    stamp = (day or date.today()).isoformat()
    with open(path, "a", encoding=ENCODING) as handle:
        handle.write(_line(f"{stamp} {entry}"))


def iter_entries(path: Path) -> Iterator[str]:
    """Stream lines lazily – memory use stays flat even for a huge file."""
    with open(path, encoding=ENCODING) as handle:
        for line in handle:
            if line.strip():
                yield line.rstrip("\n")


def read_entries(path: Path) -> list[str]:
    """EAFP: just try to open it; a missing journal is simply empty."""
    try:
        return list(iter_entries(path))
    except FileNotFoundError:
        return []


def create_new(path: Path, text: str) -> bool:
    """Mode ``"x"`` refuses to overwrite an existing file – returns False if it exists."""
    try:
        with open(path, "x", encoding=ENCODING) as handle:
            handle.write(text)
    except FileExistsError:
        return False
    return True


def atomic_write(path: Path, text: str) -> None:
    """Write to a temp file in the same folder, then ``os.replace`` it into place.

    If the program crashes mid-write, the old file is still intact.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding=ENCODING) as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_name, path)
    except BaseException:
        Path(tmp_name).unlink(missing_ok=True)
        raise


def search(path: Path, word: str) -> list[tuple[int, str]]:
    return [(n, line) for n, line in enumerate(read_entries(path), start=1) if word.lower() in line.lower()]


def main(path: Path | None = None) -> None:
    path = path or default_journal_path()
    print(f"Day 41 – Journal at {path}\n")
    write_entries(path, ["2026-04-20 Started the file I/O lesson"])
    append_entry(path, "Learned that 'w' truncates and 'a' appends", date(2026, 4, 21))
    append_entry(path, "Atomic writes protect against crashes", date(2026, 4, 22))
    for number, line in enumerate(read_entries(path), start=1):
        print(f"{number:>2}: {line}")
    print("\nSearch 'atomic':", search(path, "atomic"))
    print("Create again with mode 'x':", create_new(path, "overwrite?"))
    atomic_write(path.with_suffix(".bak"), "\n".join(read_entries(path)) + "\n")
    print("Backup lines:", len(read_entries(path.with_suffix(".bak"))))


if __name__ == "__main__":
    main()
