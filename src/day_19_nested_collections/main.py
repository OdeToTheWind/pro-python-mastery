"""Day 19 – Nested Collections.

Scenario: a *school gradebook* – classes contain students, students contain
subjects, subjects contain lists of scores.

Deliverables (syllabus):
* List of dicts
* Dict of lists
* Nested structures (safe deep access, transformation)
* A classroom management system
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from statistics import mean
from typing import Any

DELIVERABLES: dict[str, str] = {
    "list of dicts (flat records)": "build_gradebook",
    "dict of lists (scores per subject)": "subject_scores",
    "nested structure access": "deep_get",
    "classroom system operations": "add_score",
    "reporting over nested data": "class_report",
}

# gradebook[class_name][student][subject] -> list of scores
Gradebook = dict[str, dict[str, dict[str, list[int]]]]

RECORDS: list[dict[str, Any]] = [
    {"class": "10A", "student": "Aarav", "subject": "math", "score": 92},
    {"class": "10A", "student": "Aarav", "subject": "math", "score": 88},
    {"class": "10A", "student": "Aarav", "subject": "science", "score": 79},
    {"class": "10A", "student": "Diya", "subject": "math", "score": 95},
    {"class": "10A", "student": "Diya", "subject": "science", "score": 91},
    {"class": "10B", "student": "Meera", "subject": "math", "score": 67},
]


def build_gradebook(records: Sequence[Mapping[str, Any]]) -> Gradebook:
    """Convert a flat *list of dicts* into a three-level nested dict."""
    book: Gradebook = {}
    for row in records:
        add_score(book, row["class"], row["student"], row["subject"], row["score"])
    return book


def add_score(book: Gradebook, class_name: str, student: str, subject: str, score: int) -> None:
    """Insert one score, creating missing levels with ``setdefault``."""
    if not 0 <= score <= 100:
        raise ValueError(f"score must be 0–100, got {score}")
    book.setdefault(class_name, {}).setdefault(student, {}).setdefault(subject, []).append(score)


def deep_get(data: Any, path: Sequence[str | int], default: Any = None) -> Any:
    """Follow *path* through dicts/lists; return *default* at the first missing step."""
    current = data
    for key in path:
        try:
            current = current[key]
        except (KeyError, IndexError, TypeError):
            return default
    return current


def subject_scores(book: Gradebook, class_name: str) -> dict[str, list[int]]:
    """Flip the nesting: a *dict of lists* with every score per subject for one class."""
    by_subject: dict[str, list[int]] = {}
    for subjects in book.get(class_name, {}).values():
        for subject, scores in subjects.items():
            by_subject.setdefault(subject, []).extend(scores)
    return by_subject


def student_average(book: Gradebook, class_name: str, student: str) -> float | None:
    subjects = deep_get(book, [class_name, student], {})
    scores = [s for values in subjects.values() for s in values]
    return round(mean(scores), 1) if scores else None


def class_report(book: Gradebook, class_name: str) -> list[dict[str, Any]]:
    """A *list of dicts* sorted best-first – ready for printing or JSON."""
    rows = [
        {"student": student, "average": student_average(book, class_name, student),
         "subjects": sorted(subjects)}
        for student, subjects in book.get(class_name, {}).items()
    ]
    return sorted(rows, key=lambda r: r["average"] or 0, reverse=True)


def subject_toppers(book: Gradebook, class_name: str) -> dict[str, str]:
    """Best student per subject, by mean score in that subject."""
    best: dict[str, tuple[float, str]] = {}
    for student, subjects in book.get(class_name, {}).items():
        for subject, scores in subjects.items():
            avg = mean(scores)
            if subject not in best or avg > best[subject][0]:
                best[subject] = (avg, student)
    return {subject: name for subject, (_, name) in sorted(best.items())}


def main() -> None:
    book = build_gradebook(RECORDS)
    print("Day 19 – Gradebook\n")
    print("Nested:", book["10A"]["Aarav"])
    print("Deep get missing →", deep_get(book, ["10C", "Nobody", "math"], default="n/a"))
    print("Dict of lists:", subject_scores(book, "10A"))
    for row in class_report(book, "10A"):
        print(f"  {row['student']:<6} avg {row['average']:>5}  subjects: {', '.join(row['subjects'])}")
    print("Toppers:", subject_toppers(book, "10A"))


if __name__ == "__main__":
    main()
