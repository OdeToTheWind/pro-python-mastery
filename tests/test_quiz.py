"""Quality gate for the per-day quizzes in docs/quiz/ and the quiz mode of scripts/learn.py."""

import collections
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import build_reflections  # noqa: E402
import learn  # noqa: E402

COVERED = sorted(d for d, row in build_reflections.syllabus_rows().items() if row["status"] == "Covered")
QUIZZES = {day: json.loads((ROOT / "docs" / "quiz" / f"day-{day:02d}.json").read_text(encoding="utf-8"))
           for day in COVERED}
ALL_MCQ = [q for quiz in QUIZZES.values() for q in quiz["mcq"]]
PLAIN = learn.Style(enabled=False)


@pytest.mark.parametrize("day", COVERED)
def test_each_day_has_two_well_formed_mcqs(day):
    quiz = QUIZZES[day]
    assert quiz["day"] == day and len(quiz["mcq"]) == 2
    for item in quiz["mcq"]:
        assert list(item["options"]) == ["A", "B", "C", "D"]
        assert len(set(item["options"].values())) == 4, "options must be distinct"
        assert item["answer"] in item["options"]
        assert item["question"].strip() and len(item["explanation"]) > 40
        assert "option a" not in item["explanation"].lower(), "explanations must not depend on option order"


@pytest.mark.parametrize("day", COVERED)
def test_each_day_has_open_bonus_questions(day):
    bonus = QUIZZES[day]["bonus"]
    kinds = {item["type"] for item in bonus}
    assert len(bonus) >= 2 and kinds == {"discuss", "hands-on"}
    assert all(set(item) == {"type", "question"} for item in bonus), "bonus questions have no answer key"


def test_questions_are_unique_across_the_course():
    questions = [q["question"] for q in ALL_MCQ]
    assert len(questions) == len(set(questions))


def test_answer_letters_are_balanced():
    counts = collections.Counter(q["answer"] for q in ALL_MCQ)
    for letter in "ABCD":
        assert 0.2 <= counts[letter] / len(ALL_MCQ) <= 0.3, counts
    pairs = collections.Counter(tuple(q["answer"] for q in quiz["mcq"]) for quiz in QUIZZES.values())
    assert len(pairs) >= 8, "the second answer must not follow a guessable pattern"


def scripted(*answers):
    replies = iter(answers)

    def ask(_prompt):
        try:
            return next(replies)
        except StopIteration:
            raise EOFError from None

    return ask


def test_quiz_scores_correct_answers(capsys):
    key = [q["answer"] for q in QUIZZES[1]["mcq"]]
    assert learn.run_quiz(1, PLAIN, scripted(key[0].lower(), key[1])) == (2, 2)
    assert capsys.readouterr().out.count("✔ Correct!") == 2


def test_quiz_explains_wrong_answers_and_reasks_on_bad_input(capsys):
    first = QUIZZES[5]["mcq"][0]
    wrong = next(letter for letter in "ABCD" if letter != first["answer"])
    second = QUIZZES[5]["mcq"][1]["answer"]
    assert learn.run_quiz(5, PLAIN, scripted("z", "", wrong, second)) == (1, 2)
    out = capsys.readouterr().out
    assert out.count("Please type one letter") == 2
    assert f"the answer is {first['answer']}) {first['options'][first['answer']]}" in out
    assert first["explanation"][:30] in out


def test_quiz_stops_cleanly_at_end_of_input():
    assert learn.run_quiz(7, PLAIN, scripted()) == (0, 0)


def test_quiz_without_terminal_lists_questions_but_never_the_answers(capsys, monkeypatch):
    monkeypatch.setattr(learn.sys.stdin, "isatty", lambda: False, raising=False)
    assert learn.run_quiz(9, PLAIN) == (0, 0)
    out = capsys.readouterr().out
    assert QUIZZES[9]["mcq"][0]["question"][:40] in out
    assert "Correct" not in out and QUIZZES[9]["mcq"][0]["explanation"][:40] not in out


def test_bonus_questions_are_shown_without_answers(capsys):
    learn.show_bonus(12, PLAIN)
    out = capsys.readouterr().out
    assert "🧪 Hands-on" in out and "💬 Think & explain" in out and "no answers given" in out


def test_quiz_only_mode_skips_explanation_and_tests(capsys):
    assert learn.main(["3", "--quiz"]) == 0
    out = capsys.readouterr().out
    assert "Quick check" in out and "Bonus questions" in out and "Where each skill lives" not in out
