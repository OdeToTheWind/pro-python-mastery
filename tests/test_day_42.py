"""Tests for Day 42 – File Directories (sandboxed in tmp_path)."""

import pytest

from src.day_42_file_directories.main import (
    create_folder,
    find_files,
    folder_sizes,
    inside,
    list_with_os_and_pathlib,
    main,
    organise_by_extension,
    remove_folder,
    seed_downloads,
    tree,
)


@pytest.fixture
def downloads(tmp_path):
    seed_downloads(tmp_path)
    return tmp_path


def test_inside_blocks_traversal(tmp_path):
    assert inside(tmp_path, "a/b") == (tmp_path / "a" / "b").resolve()
    for escape in ("..", "../x", "a/../../x", "/etc"):
        with pytest.raises(PermissionError):
            inside(tmp_path, escape)


def test_os_and_pathlib_listings_match(downloads):
    (downloads / "sub").mkdir()
    with_os, with_pathlib = list_with_os_and_pathlib(downloads)
    assert with_os == with_pathlib
    assert "sub/" in with_os


def test_organise_by_extension(downloads):
    moved = organise_by_extension(downloads)
    assert moved == {"txt": 2, "pdf": 1, "jpg": 1, "no_extension": 1}
    assert find_files(downloads, "*.txt") == ["txt/notes.txt", "txt/todo.txt"]
    assert [p for p in downloads.iterdir() if p.is_file()] == []


def test_organise_never_overwrites(tmp_path):
    (tmp_path / "txt").mkdir()
    (tmp_path / "txt" / "a.txt").write_text("old", encoding="utf-8")
    (tmp_path / "a.txt").write_text("new", encoding="utf-8")
    organise_by_extension(tmp_path)
    assert (tmp_path / "txt" / "a.txt").read_text(encoding="utf-8") == "old"
    assert (tmp_path / "txt" / "a (1).txt").read_text(encoding="utf-8") == "new"


def test_tree_lists_folders_first(tmp_path):
    create_folder(tmp_path, "docs/old")
    (tmp_path / "a.txt").write_text("x", encoding="utf-8")
    (tmp_path / "docs" / "b.md").write_text("y", encoding="utf-8")
    assert tree(tmp_path) == [
        "├── docs/",
        "│   ├── old/",
        "│   └── b.md",
        "└── a.txt",
    ]


def test_folder_sizes(tmp_path):
    create_folder(tmp_path, "sub")
    (tmp_path / "a").write_bytes(b"12345")
    (tmp_path / "sub" / "b").write_bytes(b"12")
    assert folder_sizes(tmp_path) == {".": 5, "sub": 2}


def test_remove_folder_requires_consent_for_non_empty(tmp_path):
    folder = create_folder(tmp_path, "full")
    (folder / "file").write_text("x", encoding="utf-8")
    with pytest.raises(OSError, match="not empty"):
        remove_folder(tmp_path, "full")
    remove_folder(tmp_path, "full", recursive=True)
    assert not folder.exists()


def test_remove_folder_guards(tmp_path):
    create_folder(tmp_path, "empty")
    remove_folder(tmp_path, "empty")
    with pytest.raises(FileNotFoundError):
        remove_folder(tmp_path, "empty")
    with pytest.raises(PermissionError):
        remove_folder(tmp_path, ".", recursive=True)
    with pytest.raises(PermissionError):
        remove_folder(tmp_path, "../", recursive=True)


def test_main(capsys):
    main()
    out = capsys.readouterr().out
    assert "os vs pathlib agree: True" in out
    assert "Refused: 'txt' is not empty" in out
    assert "Blocked traversal: ../../etc" in out
