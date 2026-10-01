#!/usr/bin/env bash
# Local quality gate – runs exactly what CI runs.
#
#   ./propython.sh            lint + type-check + regenerate docs + tests with coverage
#   ./propython.sh --commit   …then show `git status`, ask for a message, commit and
#                             push the *current* branch (never a hard-coded one)
set -euo pipefail

echo "------------------------------------------"
echo "🐍 PRO PYTHON MASTERY: ENGINEERING CHECK"
echo "------------------------------------------"

if [[ -z "${VIRTUAL_ENV:-}" ]]; then
    for activate in .venv/bin/activate .venv/Scripts/activate; do
        if [[ -f "$activate" ]]; then
            # shellcheck disable=SC1090
            source "$activate"
            echo "🔧 Activated $activate"
            break
        fi
    done
fi

echo "🔎 ruff";  ruff check src tests scripts
echo "🧠 mypy";  mypy src
echo "📝 reflections"; python scripts/build_reflections.py
echo "🧪 pytest"; python -m pytest -m "not network" --cov=src --cov-report=term --cov-fail-under=85 -q

if ! git diff --quiet -- docs/progress README.md; then
    echo "⚠️  Reflections/README were regenerated – review and commit them."
fi
echo "✅ All checks passed."

if [[ "${1:-}" == "--commit" ]]; then
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
fi
