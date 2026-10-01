"""Day 40 – Python Slice Function.

Scenario: a *bank-statement parser* for fixed-width text records, plus a
playlist editor – both lean on slicing.

Deliverables (syllabus):
* Advanced slicing of strings (fixed-width fields, steps, reversal)
* Advanced slicing of lists (slice assignment, deletion, rotation, chunking)
* The built-in ``slice()`` object (named slices, ``slice.indices``)
"""

from __future__ import annotations

from collections.abc import Sequence

DELIVERABLES: dict[str, str] = {
    "slice() objects as named fields": "parse_record",
    "slice.indices()": "describe_slice",
    "string slicing: steps and reversal": "mask_account",
    "list slicing: assignment": "replace_section",
    "list slicing: deletion": "drop_every_other",
    "rotation and chunking": "rotate",
    "guarding against step=0": "safe_slice",
}

# A statement line looks like: "2026-04-21 GB29NWBK60161331926819 -0000123.45 COFFEE"
DATE = slice(0, 10)
ACCOUNT = slice(11, 33)
AMOUNT = slice(34, 45)
MEMO = slice(46, None)


def parse_record(line: str) -> dict[str, str | float]:
    """Named ``slice`` objects make fixed-width parsing self-documenting."""
    if len(line) < MEMO.start:
        raise ValueError("record too short")
    return {
        "date": line[DATE],
        "account": line[ACCOUNT],
        "amount": float(line[AMOUNT]),
        "memo": line[MEMO].strip(),
    }


def mask_account(account: str, visible: int = 4) -> str:
    """Keep the last *visible* characters: negative indices count from the end."""
    if visible <= 0:
        return "•" * len(account)
    return "•" * len(account[:-visible]) + account[-visible:]


def is_palindrome(text: str) -> bool:
    letters = "".join(ch for ch in text.casefold() if ch.isalnum())
    return letters == letters[::-1]


def safe_slice[T](seq: Sequence[T], start: int | None, stop: int | None, step: int | None = None) -> Sequence[T]:
    if step == 0:
        raise ValueError("slice step cannot be zero")
    return seq[start:stop:step]


def describe_slice(s: slice, length: int) -> tuple[int, int, int]:
    """Resolve ``None``/negative/out-of-range bounds for a sequence of *length*."""
    return s.indices(length)


def replace_section[T](items: list[T], start: int, stop: int, new: list[T]) -> list[T]:
    """Slice *assignment* can change a list's length in place."""
    result = list(items)
    result[start:stop] = new
    return result


def drop_every_other[T](items: list[T]) -> list[T]:
    """``del lst[1::2]`` removes items at odd positions in one statement."""
    result = list(items)
    del result[1::2]
    return result


def rotate[T](items: Sequence[T], k: int) -> list[T]:
    """Rotate left by *k* (negative rotates right) using two slices."""
    if not items:
        return []
    k %= len(items)
    return list(items[k:]) + list(items[:k])


def chunk[T](items: Sequence[T], size: int) -> list[Sequence[T]]:
    if size < 1:
        raise ValueError("size must be positive")
    return [items[i : i + size] for i in range(0, len(items), size)]


SAMPLE = [
    "2026-04-21 GB29NWBK60161331926819 -0000003.40 COFFEE",
    "2026-04-22 GB29NWBK60161331926819 +0002500.00 SALARY",
]


def main() -> None:
    print("Day 40 – Statements and playlists\n")
    for line in SAMPLE:
        record = parse_record(line)
        print(f"{record['date']} {mask_account(str(record['account']))} {record['amount']:>9.2f} {record['memo']}")
    print("slice(-3, None).indices(10) →", describe_slice(slice(-3, None), 10))
    playlist = ["intro", "song A", "song B", "ad", "song C", "ad", "outro"]
    print("reversed:", playlist[::-1])
    print("replace middle:", replace_section(playlist, 1, 3, ["remix"]))
    print("every other dropped:", drop_every_other(playlist))
    print("rotate 2:", rotate(playlist, 2))
    print("chunks of 3:", chunk(playlist, 3))
    print("palindrome 'Never odd or even'?", is_palindrome("Never odd or even"))


if __name__ == "__main__":
    main()
