# Contributing to Pro Python Mastery

Thank you for helping. A clearer sentence, an extra edge-case test or a fixed typo is
a real contribution, and every contribution makes the course better for the next learner.

By taking part you agree to follow the [Code of Conduct](CODE_OF_CONDUCT.md).

## Ways to contribute

| You want to… | Do this |
|---|---|
| Report a mistake in a lesson | Open a **Content error** issue: say which day, what's wrong and what you expected. |
| Report broken code or a failing test | Open a **Bug report** issue with the command, your OS, your Python version and the output. |
| Suggest a new exercise or scenario | Open an **Idea** issue before writing code, so we can agree on the scope first. |
| Fix something yourself | Fork the repository, make a branch, and open a pull request (see below). |

## Set up your environment

```bash
git clone https://github.com/<your-username>/pro-python-mastery.git
cd pro-python-mastery
python -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
./propython.sh --check               # must end with "All checks passed"
```

Python 3.12 or newer is required. CI runs Python 3.12, 3.13 and 3.14 on Linux, plus
Python 3.14 on Windows and macOS.

## How a day is built

Every day follows the same contract, and `tests/test_syllabus_sync.py` checks it.

```text
src/day_XX_<topic>/
├── __init__.py
└── main.py                 # docstring with "Scenario:", DELIVERABLES dict, functions, main()
tests/test_day_XX.py        # at least 5 tests; imports src.day_XX_<topic>.main
docs/progress/notes/day-XX.json        # hand-written learnings, pitfalls, next step
docs/progress/day-XX-reflection.md     # GENERATED, so never edit it by hand
docs/quiz/day-XX.json                  # 2 multiple-choice questions + bonus questions
```

Rules that keep the course trustworthy:

1. **One scenario per day.** The `Scenario:` line in the module docstring must be unique across all 100 days.
2. **Every deliverable maps to code.** Each syllabus deliverable gets an entry in `DELIVERABLES` that resolves to a real function, class or constant.
3. **Tests teach.** Test real behaviour and edge cases. `assert True` and tests that only check that code runs are rejected.
4. **No network in tests.** Use `tmp_path`, mocks, or a local server on `127.0.0.1`.
5. **Secrets stay out of code.** Read them from the environment; never commit a `.env` file.
6. **Quizzes test this day's code.** Each `docs/quiz/day-XX.json` has exactly 2 multiple-choice
   questions (options A–D, one correct answer, an explanation that doesn't depend on option
   order) and at least one *discuss* and one *hands-on* bonus question, with no answer key.
   `tests/test_quiz.py` also keeps the correct letters balanced across the course.
7. **Generated files are generated.** After you change notes, docstrings, `syllabus.md` or the tests, run
   `python scripts/build_reflections.py`. It rewrites the reflections and the generated blocks in the README.

## Style

* Formatting and lint: `ruff check src tests scripts` (configuration in `pyproject.toml`).
* Types: `mypy src` must pass. Public functions have type hints and a docstring.
* Keep modules readable for learners: explicit names, short functions, a comment only where the *why* isn't obvious.
* Use British or American spelling consistently within a file.

## Pull requests

1. Create a branch: `git switch -c fix/day-18-dict-merge-typo`.
2. Make one focused change. Smaller pull requests are reviewed faster.
3. Run `./propython.sh --check` and make sure it passes and leaves no uncommitted generated files.
4. Write a commit message that says *what* changed and *why*.
5. Open the pull request and fill in the template.

A maintainer will review within a week. CI must be green before a merge.

## Licensing of contributions

By submitting a contribution you agree that it is licensed under the [MIT License](LICENSE.md),
the same terms as the rest of the project.
