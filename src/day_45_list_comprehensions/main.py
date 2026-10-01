"""Day 45 – List Comprehensions.

Scenario: a *web-server log analyser* – raw access-log lines become clean,
filtered, transformed lists in one readable expression each.

Deliverables (syllabus):
* Concise creation of lists
* Filtering (``if`` clause)
* Transformation (expressions, conditional expressions, nesting, walrus)
"""

from __future__ import annotations

import re
import sys

DELIVERABLES: dict[str, str] = {
    "creation": "status_codes",
    "filtering": "server_errors",
    "transformation": "normalise_paths",
    "conditional expression inside": "status_labels",
    "nested comprehension (flatten / matrix)": "transpose",
    "walrus operator in a comprehension": "slow_requests",
    "comprehension vs loop vs generator": "loop_equivalent",
}

LOG = [
    '10.0.0.1 - - [21/Apr/2026:10:00:01] "GET /Index.html HTTP/1.1" 200 512 0.020',
    '10.0.0.2 - - [21/Apr/2026:10:00:02] "GET /api/users?id=7 HTTP/1.1" 500 128 1.540',
    '10.0.0.1 - - [21/Apr/2026:10:00:03] "POST /api/login HTTP/1.1" 401 64 0.110',
    "malformed line",
    '10.0.0.3 - - [21/Apr/2026:10:00:04] "GET /images/logo.PNG HTTP/1.1" 304 0 0.003',
    '10.0.0.2 - - [21/Apr/2026:10:00:05] "GET /api/orders HTTP/1.1" 503 90 2.900',
]
PATTERN = re.compile(r'"(?P<method>\w+) (?P<path>\S+) [^"]+" (?P<status>\d{3}) \d+ (?P<secs>[\d.]+)')


def parse(lines: list[str]) -> list[re.Match[str]]:
    """Creation + filtering: keep only lines the pattern understands."""
    return [m for line in lines if (m := PATTERN.search(line))]


def status_codes(lines: list[str]) -> list[int]:
    return [int(m["status"]) for m in parse(lines)]


def server_errors(lines: list[str]) -> list[str]:
    return [m["path"] for m in parse(lines) if int(m["status"]) >= 500]


def normalise_paths(lines: list[str]) -> list[str]:
    """Transformation: lowercase and drop the query string."""
    return [m["path"].split("?", 1)[0].lower() for m in parse(lines)]


def status_labels(codes: list[int]) -> list[str]:
    """Conditional expression *in the output* (different from a filter)."""
    return ["ok" if c < 300 else "redirect" if c < 400 else "client" if c < 500 else "server" for c in codes]


def slow_requests(lines: list[str], threshold: float) -> list[tuple[str, float]]:
    """Walrus: compute once, use it in both the filter and the output."""
    return [(m["path"], secs) for m in parse(lines) if (secs := float(m["secs"])) > threshold]


def transpose(matrix: list[list[int]]) -> list[list[int]]:
    """Nested comprehension: rows become columns."""
    if not matrix:
        return []
    return [[row[col] for row in matrix] for col in range(len(matrix[0]))]


def flatten(matrix: list[list[int]]) -> list[int]:
    """Read nested ``for`` clauses left-to-right like nested loops."""
    return [value for row in matrix for value in row]


def loop_equivalent(lines: list[str]) -> list[str]:
    """The same as ``server_errors`` written as a loop – longer and easier to get wrong."""
    result = []
    for m in parse(lines):
        if int(m["status"]) >= 500:
            result.append(m["path"])
    return result


def memory_comparison(n: int) -> tuple[int, int]:
    """A list materialises every item; a generator expression stays tiny."""
    as_list = [i * i for i in range(n)]
    as_generator = (i * i for i in range(n))
    return sys.getsizeof(as_list), sys.getsizeof(as_generator)


def main() -> None:
    print("Day 45 – Log analyser\n")
    codes = status_codes(LOG)
    print("status codes:", codes)
    print("labels      :", status_labels(codes))
    print("5xx paths   :", server_errors(LOG))
    print("normalised  :", normalise_paths(LOG))
    print("slow (>1s)  :", slow_requests(LOG, 1.0))
    print("transpose   :", transpose([[1, 2, 3], [4, 5, 6]]))
    print("list vs generator bytes for 10 000 items:", memory_comparison(10_000))


if __name__ == "__main__":
    main()
