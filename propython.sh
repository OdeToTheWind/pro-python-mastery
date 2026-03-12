#!/bin/bash

# 1. Run the Python Code
echo "🚀 Running Day 1 Logic..."
python src/day_01_variables/main.py

# 2. Run the Tests using the python module runner
echo "🧪 Running Tests..."
python -m pytest

if [ $? -ne 0 ]; then
    echo "❌ Tests failed! Fix your code before pushing."
    exit 1
fi

# 3. Git Automation
echo "📝 Enter your commit message:"
read commit_message

git add .
git commit -m "$commit_message"
git push .
git push -u origin master

echo "✅ Successfully tested and pushed to GitHub!"