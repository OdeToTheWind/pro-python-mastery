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
    else
        echo "⚠️  Virtual environment found but activate script missing."
    fi
fi

# ====================== RUN DAYS 46 TO 56 ======================
echo "🚀 Running Days 46 to 56 (Main Modules)..."

for day in {46..56}; do
    # More precise and robust directory matching
    dir=$(find src -maxdepth 1 -type d -name "day_${day}_*" | head -n 1)
    
    if [ -n "$dir" ]; then
        # Convert path to module (e.g. src/day_46_advanced -> src.day_46_advanced)
        module=$(echo "$dir" | sed 's/\//./g')
        
        echo "──────────────────────────────────────────"
        echo "Running Day $day → $module.main"
        echo "──────────────────────────────────────────"
        
        # Run the main entry point
        python -m "${module}.main"
        
        if [ $? -ne 0 ]; then
            echo "❌ Day $day failed!"
            deactivate 2>/dev/null || true
            exit 1
        fi
        
        echo "✅ Day $day completed successfully"
        echo ""
    else
        echo "⚠️  Directory for Day $day not found (skipped)"
    fi
done

# ====================== TEST SUITE ======================
echo "🧪 Running Comprehensive Test Suite..."
python -m pytest -v --tb=short

if [ $? -ne 0 ]; then
    echo "❌ Some tests failed! Fix them before pushing."
    deactivate 2>/dev/null || true
    exit 1
fi

echo "✅ All tests passed!"

# ====================== GIT COMMIT & PUSH ======================
echo "📝 Enter commit message for Days 46-56:"
read -r commit_message

git add .
git commit -m "Days 46-56: $commit_message"
git push origin master

echo "✅ Successfully tested, committed and pushed!"

# Cleanup
deactivate 2>/dev/null || true
echo "🎉 Done."