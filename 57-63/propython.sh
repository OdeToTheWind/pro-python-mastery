#!/usr/bin/env bash
set -euo pipefail

echo "------------------------------------------"
echo "🐍 PRO PYTHON MASTERY: ENGINEERING CHECK"
echo "------------------------------------------"

# ====================== VIRTUAL ENVIRONMENT ======================
VENV_PATH=".venv"
if [ -d "$VENV_PATH" ]; then
    echo "🔧 Activating virtual environment..."
    if [ -f "$VENV_PATH/Scripts/activate" ]; then
        # Windows-style venv
        # shellcheck disable=SC1091
        source "$VENV_PATH/Scripts/activate"
    elif [ -f "$VENV_PATH/bin/activate" ]; then
        # Unix-style venv
        # shellcheck disable=SC1091
        source "$VENV_PATH/bin/activate"
    else
        echo "⚠️  Virtual environment found but activate script missing."
    fi
else
    echo "ℹ️  No virtual environment found at $VENV_PATH (continuing with system Python)"
fi

# ====================== RUN DAYS 57 TO 63 ======================
echo "🚀 Running Days 57 to 63 (Intermediate Projects – API clients, automation & data acquisition)..."

for day in {57..63}; do
    # More precise and robust directory matching
    dir=$(find src -maxdepth 1 -type d -name "day_${day}_*" 2>/dev/null | head -n 1)

    if [ -n "$dir" ]; then
        # Convert path to module (e.g. src/day_57_rest_apis_json -> src.day_57_rest_apis_json)
        module=$(echo "$dir" | sed 's/\//./g')

        echo "──────────────────────────────────────────"
        echo "Running Day $day → ${module}.main"
        echo "──────────────────────────────────────────"

        # Run the main entry point
        if python -m "${module}.main"; then
            echo "✅ Day $day completed successfully"
            echo ""
        else
            echo "❌ Day $day failed!"
            deactivate 2>/dev/null || true
            exit 1
        fi
    else
        echo "⚠️  Directory for Day $day not found (skipped)"
    fi
done

# ====================== TEST SUITE ======================
echo "🧪 Running Comprehensive Test Suite (Days 57–63)..."
python -m pytest tests/ -v --tb=short 

if [ $? -ne 0 ]; then
    echo "❌ Some tests failed! Fix them before pushing."
    deactivate 2>/dev/null || true
    exit 1
fi

echo "✅ All tests passed!"

# ====================== GIT COMMIT & PUSH ======================
if [ -d .git ]; then
    echo "📝 Enter commit message for Days 57-63:"
    read -r commit_message

    git add .
    git commit -m "Days 57-63: $commit_message" || echo "⚠️  Nothing to commit or commit failed"
    git push origin master || echo "⚠️  Push failed (check remote / branch)"
    echo "✅ Successfully tested, committed and pushed!"
else
    echo "ℹ️  Not a git repository – skipping commit/push"
fi

# Cleanup
deactivate 2>/dev/null || true
echo "🎉 Done."
