#!/bin/bash

# 1. Find the latest day directory
# Result example: src/day_02_strings/
LATEST_PATH=$(ls -d src/day_*/ | sort -V | tail -n 1)

# 2. Convert path to module notation
# Remove trailing slash, then change / to .
# Result example: src.day_02_strings.main
LATEST_MODULE=$(echo "${LATEST_PATH%/}" | tr '/' '.')

echo "------------------------------------------"
echo "🐍 PRO PYTHON MASTERY: ENGINEERING CHECK"
echo "------------------------------------------"

# 3. Run the latest Python Code
echo "🚀 Executing latest logic: $LATEST_MODULE.main"
python -m "$LATEST_MODULE.main"

echo ""
# 4. Run the Tests
echo "🧪 Running Comprehensive Test Suite..."
python -m pytest -v

if [ $? -ne 0 ]; then
    echo "❌ Tests failed! Fix your code before pushing."
    exit 1
fi

# 5. Git Automation
# Using basename to get 'day_02_strings' instead of the full path
DAY_NAME=$(basename "$LATEST_PATH")

echo "📝 Enter your commit message for $DAY_NAME:"
read commit_message

git add .
git commit -m "$DAY_NAME: $commit_message"
git push origin master

echo "✅ Successfully tested and pushed to GitHub!"