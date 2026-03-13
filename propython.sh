#!/usr/bin/env bash

echo "------------------------------------------"
echo "🐍 PRO PYTHON MASTERY: ENGINEERING CHECK"
echo "------------------------------------------"

# 1. Find the latest day directory (e.g. src/day_02_strings/)
LATEST_PATH=$(ls -d src/day_*/ 2>/dev/null | sort -V | tail -n 1)

if [ -z "$LATEST_PATH" ]; then
    echo "❌ No day_* directory found in src/"
    exit 1
fi

# 2. Convert to module path (src.day_02_strings)
LATEST_MODULE=$(echo "${LATEST_PATH%/}" | tr '/' '.')

echo "🚀 Executing latest logic: $LATEST_MODULE.main"
python -m "$LATEST_MODULE.main"

# Optional: suppress the warning (not needed after fix)
# PYTHONWARNINGS=ignore::RuntimeWarning python -m ...

echo ""
echo "🧪 Running Comprehensive Test Suite..."
python -m pytest -v

if [ $? -ne 0 ]; then
    echo "❌ Tests failed! Fix your code before pushing."
    exit 1
fi

# 5. Git Automation
DAY_NAME=$(basename "$LATEST_PATH")
echo "📝 Enter your commit message for $DAY_NAME:"
read -r commit_message

git add .
git commit -m "$DAY_NAME: $commit_message"
git push origin master

echo "✅ Successfully tested and pushed to GitHub!"