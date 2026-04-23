#!/usr/bin/env bash

echo "------------------------------------------"
echo "🐍 PRO PYTHON MASTERY: ENGINEERING CHECK"
echo "------------------------------------------"

# ====================== VIRTUAL ENVIRONMENT HANDLING ======================
VENV_PATH=".venv"

if [ -d "$VENV_PATH" ]; then
    echo "🔧 Activating virtual environment..."

    # Windows Git Bash / MSYS2
    if [ -f "$VENV_PATH/Scripts/activate" ]; then
        source "$VENV_PATH/Scripts/activate"
    # Linux / macOS
    elif [ -f "$VENV_PATH/bin/activate" ]; then
        source "$VENV_PATH/bin/activate"
    else
        echo "⚠️  Virtual environment found but activation script missing."
    fi
else
    echo "⚠️  Virtual environment not found at $VENV_PATH"
    echo "   Create it with: python -m venv .venv"
fi

# ====================== FIND LATEST DAY ======================
LATEST_PATH=$(ls -d src/day_*/ 2>/dev/null | sort -V | tail -n 1)

if [ -z "$LATEST_PATH" ]; then
    echo "❌ No day_* directory found in src/"
    exit 1
fi

LATEST_MODULE=$(echo "${LATEST_PATH%/}" | tr '/' '.')

echo "🚀 Executing latest logic: $LATEST_MODULE.main"
python -m "$LATEST_MODULE.main"

echo ""
echo "🧪 Running Comprehensive Test Suite..."
python -m pytest -v

if [ $? -ne 0 ]; then
    echo "❌ Tests failed! Fix your code before pushing."
    deactivate 2>/dev/null || true
    exit 1
fi

# ====================== GIT AUTOMATION ======================
DAY_NAME=$(basename "$LATEST_PATH")
echo "📝 Enter your commit message for $DAY_NAME:"
read -r commit_message

git add .
git commit -m "$DAY_NAME: $commit_message"
git push origin master

echo "✅ Successfully tested and pushed to GitHub!"

# ====================== CLEAN UP ======================
echo "🔌 Deactivating virtual environment..."
deactivate 2>/dev/null || true

echo "Done."