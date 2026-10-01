"""Day 42 – File Directories.

Scenario: a *downloads-folder organiser* – it scaffolds folders, prints a tree,
finds files by pattern, sorts files into folders by extension and cleans up,
all confined to one sandbox root so a typo can never touch the rest of the disk.

Deliverables (syllabus):
* ``os`` and ``pathlib`` (side by side)
* Folder navigation (walking, globbing, tree listing)
* File-system work (create, move, remove – safely)
"""

from __future__ import annotations

import os
import shutil
from collections import Counter
from pathlib import Path

DELIVERABLES: dict[str, str] = {
    "os vs pathlib": "list_with_os_and_pathlib",
    "navigation: tree listing": "tree",
    "navigation: os.walk": "folder_sizes",
    "navigation: glob / rglob": "find_files",
    "file-system work: create": "create_folder",
    "file-system work: move": "organise_by_extension",
    "file-system work: safe removal": "remove_folder",
    "path traversal protection": "inside",
}


def inside(root: Path, relative: str | Path) -> Path:
    """Resolve *relative* under *root*; refuse anything that escapes it (``../``)."""
    root = root.resolve()
    target = (root / relative).resolve()
    if not target.is_relative_to(root):
        raise PermissionError(f"{relative!s} is outside {root}")
    return target


def create_folder(root: Path, relative: str) -> Path:
    folder = inside(root, relative)
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def remove_folder(root: Path, relative: str, *, recursive: bool = False) -> None:
    """Remove a folder. Non-empty folders need ``recursive=True`` (explicit consent)."""
    folder = inside(root, relative)
    if folder == root.resolve():
        raise PermissionError("refusing to delete the sandbox root")
    if not folder.is_dir():
        raise FileNotFoundError(f"no folder {relative!r}")
    if any(folder.iterdir()) and not recursive:
        raise OSError(f"{relative!r} is not empty – pass recursive=True to delete it")
    shutil.rmtree(folder) if recursive else folder.rmdir()


def list_with_os_and_pathlib(folder: Path) -> tuple[list[str], list[str]]:
    """The same listing written with ``os`` and with ``pathlib``."""
    with_os = sorted(
        name + ("/" if os.path.isdir(os.path.join(folder, name)) else "") for name in os.listdir(folder)
    )
    with_pathlib = sorted(p.name + ("/" if p.is_dir() else "") for p in folder.iterdir())
    return with_os, with_pathlib


def tree(folder: Path, prefix: str = "") -> list[str]:
    """Recursive tree with folders first, like the ``tree`` command."""
    entries = sorted(folder.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))
    lines: list[str] = []
    for index, entry in enumerate(entries):
        last = index == len(entries) - 1
        lines.append(f"{prefix}{'└── ' if last else '├── '}{entry.name}{'/' if entry.is_dir() else ''}")
        if entry.is_dir():
            lines.extend(tree(entry, prefix + ("    " if last else "│   ")))
    return lines


def find_files(root: Path, pattern: str) -> list[str]:
    """Recursive glob, returned as POSIX-style paths relative to *root*."""
    return sorted(p.relative_to(root).as_posix() for p in root.rglob(pattern) if p.is_file())


def folder_sizes(root: Path) -> dict[str, int]:
    """Bytes per directory using ``os.walk`` (top-down traversal)."""
    sizes: dict[str, int] = {}
    for dirpath, _dirnames, filenames in os.walk(root):
        rel = Path(dirpath).relative_to(root).as_posix()
        sizes[rel] = sum(os.path.getsize(os.path.join(dirpath, f)) for f in filenames)
    return sizes


def organise_by_extension(root: Path) -> Counter[str]:
    """Move loose files in *root* into sub-folders named after their extension."""
    moved: Counter[str] = Counter()
    for file in [p for p in root.iterdir() if p.is_file()]:
        ext = file.suffix.lower().lstrip(".") or "no_extension"
        target_dir = create_folder(root, ext)
        destination = target_dir / file.name
        counter = 1
        while destination.exists():  # never overwrite an existing file
            destination = target_dir / f"{file.stem} ({counter}){file.suffix}"
            counter += 1
        file.rename(destination)
        moved[ext] += 1
    return moved


def seed_downloads(root: Path) -> None:
    for name, content in {"report.PDF": "%PDF", "photo.jpg": "img", "notes.txt": "hi",
                          "todo.txt": "buy milk", "README": "no ext"}.items():
        (root / name).write_text(content, encoding="utf-8")


def main(root: Path | None = None) -> None:
    import tempfile

    print("Day 42 – Downloads organiser\n")
    with tempfile.TemporaryDirectory() as tmp:
        sandbox = root or Path(tmp)
        seed_downloads(sandbox)
        print("os vs pathlib agree:", len(set(map(tuple, list_with_os_and_pathlib(sandbox)))) == 1)
        print("Moved:", dict(organise_by_extension(sandbox)))
        create_folder(sandbox, "archive/2026")
        print("\n".join(["."] + tree(sandbox)))
        print("*.txt files:", find_files(sandbox, "*.txt"))
        print("Sizes:", folder_sizes(sandbox))
        try:
            remove_folder(sandbox, "txt")
        except OSError as exc:
            print("Refused:", exc)
        try:
            inside(sandbox, "../../etc")
        except PermissionError as exc:
            print("Blocked traversal:", exc.args[0].split(" is outside")[0])


if __name__ == "__main__":
    main()
