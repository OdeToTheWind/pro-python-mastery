"""Tests for Day 26 – PyCharm Tips and Tricks."""

import pytest

from src.day_26_pycharm_tips_tricks.main import (
    SHORTCUTS,
    cheat_sheet,
    expand_template,
    find_shortcuts,
    main,
    safe_rename,
)


def test_find_shortcuts_by_action_and_os():
    assert find_shortcuts("rename") == ["Rename: Shift+F6"]
    assert find_shortcuts("RENAME", "mac") == ["Rename: ⇧F6"]


def test_find_shortcuts_by_category():
    debugging = find_shortcuts("debugging")
    assert len(debugging) == sum(s.category == "debugging" for s in SHORTCUTS) == 5


def test_every_shortcut_has_both_os_bindings():
    assert all(s.windows_linux and s.macos for s in SHORTCUTS)
    assert len({s.action for s in SHORTCUTS}) == len(SHORTCUTS)


def test_expand_template():
    assert expand_template("main", end="run()") == 'if __name__ == "__main__":\n    run()'
    assert expand_template("prop", name="price") == "@property\ndef price(self):\n    return self._price"
    assert expand_template("iter") == "for $VAR$ in $ITERABLE$:\n    pass"
    with pytest.raises(KeyError):
        expand_template("nope")


def test_safe_rename_only_touches_identifiers():
    code = "total = 1\nsubtotal = total + 1  # total\nprint('total', total)\n"
    renamed = safe_rename(code, "total", "amount")
    assert renamed == "amount = 1\nsubtotal = amount + 1  # total\nprint('total', amount)\n"
    compile(renamed, "<renamed>", "exec")


@pytest.mark.parametrize("bad", ["class", "2x", "my-name"])
def test_safe_rename_rejects_invalid_names(bad):
    with pytest.raises(ValueError):
        safe_rename("x = 1\n", "x", bad)


def test_cheat_sheet_numbering_is_not_duplicated():
    sheet = cheat_sheet()
    assert "1. 1." not in sheet
    assert "NAVIGATION" in sheet and "  1. Search everywhere" in sheet
    assert "⌘B" in cheat_sheet("macos")


def test_main(capsys):
    main()
    assert "for user in users:" in capsys.readouterr().out
