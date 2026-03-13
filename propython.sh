#!/bin/bash

# Find the latest day directory automatically
LATEST_DAY=$(ls -d src/day_*/ | sort -V | tail -n 1)

echo "------------------------------------------"
echo "🐍 PRO PYTHON MASTERY: ENGINEERING CHECK"
echo "------------------------------------------"

# 1. Run the latest Python Code
echo "🚀 Executing latest logic in: $LATEST_DAY"
# Use -m to run it as a module so relative imports work correctly
python -m "${LATEST_DAY%/}/main"

echo ""
# 2. Run the Tests
echo "🧪 Running Comprehensive Test Suite..."
# Using -v for verbose output to see which tests pass
python -m pytest -v

if [ $? -ne 0 ]; then
    echo "❌ Tests failed! Fix your code before pushing."
    exit 1
fi

# 3. Git Automation
echo "📝 Enter your commit message for Day $(basename $LATEST_DAY):"
read commit_message

git add .
git commit -m "Day $(basename $LATEST_DAY): $commit_message"

# Note: 'git push .' is usually not needed if pushing to origin
git push origin master

echo "✅ Successfully tested and pushed to GitHub!"