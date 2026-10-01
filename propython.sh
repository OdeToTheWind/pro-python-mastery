#!/usr/bin/env bash
# Pro Python Mastery – study a day, or run the full quality gate.
#
#   ./propython.sh              menu: pick a day to study, or run the full check
#   ./propython.sh 18           study Day 18: explanation, code map, notes, tests, quiz, bonus questions
#   ./propython.sh 18 --quiz    only the quiz (2 multiple-choice questions) and the bonus questions
#   ./propython.sh 18 --demo    …and run the day's demo straight away
#   ./propython.sh --check      lint + type-check + regenerate docs + all tests with coverage (= CI)
#   ./propython.sh --commit     full check, then commit and push the *current* branch
#
# With no arguments and no terminal (e.g. in a script), it runs --check.
set -euo pipefail
cd "$(dirname "$0")"

if [[ -z "${VIRTUAL_ENV:-}" ]]; then
    for activate in .venv/bin/activate .venv/Scripts/activate; do
        if [[ -f "$activate" ]]; then
            # shellcheck disable=SC1090
            source "$activate"
            break
        fi
    done
fi
PYTHON="$(command -v python || command -v python3)"

full_check() {
    echo "------------------------------------------"
    echo "🐍 PRO PYTHON MASTERY: ENGINEERING CHECK"
    echo "------------------------------------------"
    echo "🔎 ruff";  ruff check src tests scripts
    echo "🧠 mypy";  mypy src
    echo "📝 reflections"; "$PYTHON" scripts/build_reflections.py
    echo "🧪 pytest"; "$PYTHON" -m pytest -m "not network" --cov=src --cov-report=term --cov-fail-under=85 -q
    if ! git diff --quiet -- docs/progress README.md; then
        echo "⚠️  Reflections/README were regenerated – review and commit them."
    fi
    echo "✅ All checks passed."
}

commit_and_push() {
    branch="$(git rev-parse --abbrev-ref HEAD)"
    git status --short
    if git ls-files --others --exclude-standard | grep -qE '(^|/)\.env$'; then
        echo "❌ A .env file is about to be committed – aborting." >&2
        exit 1
    fi
    read -r -p "Commit message for '$branch': " message
    [[ -n "$message" ]] || { echo "Empty message – nothing committed."; exit 1; }
    git add -A
    git commit -m "$message"
    git push -u origin "$branch"
}

menu() {
    echo "------------------------------------------"
    echo "🐍 PRO PYTHON MASTERY"
    echo "------------------------------------------"
    echo "  1–100   study that day (explanation, code map, notes, tests, quiz)"
    echo "  c       run the full quality check (same as CI)"
    echo "  q       quit"
    read -r -p "Your choice: " choice
    case "$choice" in
        q|Q|"") exit 0 ;;
        c|C) full_check ;;
        *[!0-9]*) echo "Please enter a day number, c or q." >&2; exit 2 ;;
        *) exec "$PYTHON" scripts/learn.py "$choice" ;;
    esac
}

case "${1:-}" in
    --check|--all) full_check ;;
    --commit) full_check; commit_and_push ;;
    -h|--help) sed -n '2,11p' "$0" | sed 's/^# \{0,1\}//' ;;
    "") if [[ -t 0 ]]; then menu; else full_check; fi ;;
    *[!0-9]*) echo "Unknown option '$1' – try ./propython.sh --help" >&2; exit 2 ;;
    *) exec "$PYTHON" scripts/learn.py "$@" ;;
esac
