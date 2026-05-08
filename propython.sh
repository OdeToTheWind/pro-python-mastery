#!/usr/bin/env bash

echo "------------------------------------------"
echo "🐍 PRO PYTHON MASTERY: ENGINEERING CHECK"
echo "------------------------------------------"

# ====================== VIRTUAL ENVIRONMENT ======================
VENV_PATH=".venv"

if [ -d "$VENV_PATH" ]; then
    echo "🔧 Activating virtual environment..."
    if [ -f "$VENV_PATH/Scripts/activate" ]; then
        source "$VENV_PATH/Scripts/activate"
    elif [ -f "$VENV_PATH/bin/activate" ]; then
        source "$VENV_PATH/bin/activate"
    fi
fi

# ====================== RUN DAYS 36 TO 45 ======================
echo "🚀 Running Days 36 to 45 (Intermediate Section)..."

for day in {36..45}; do
    dir="src/day_${day}_"*
    if [ -d "$dir" ]; then
        module=$(echo "${dir%/}" | tr '/' '.')
        echo "──────────────────────────────────────────"
        echo "Running Day $day: $module"
        echo "──────────────────────────────────────────"
        python -m "$module.main"
        echo ""
    fi
done

echo "🧪 Running Comprehensive Test Suite..."
python -m pytest -v

if [ $? -ne 0 ]; then
    echo "❌ Tests failed! Fix your code before pushing."
    deactivate 2>/dev/null || true
    exit 1
fi

# ====================== GIT ======================
echo "📝 Enter commit message for Days 36-45:"
read -r commit_message

git add .
git commit -m "Days 36-45: $commit_message"
git push origin master

echo "✅ Successfully tested and pushed!"

# Deactivate venv
deactivate 2>/dev/null || true
echo "Done."