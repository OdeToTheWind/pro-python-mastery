# src/day_26_pycharm_tips_tricks/main.py
"""
Day 26: PyCharm Tips and Tricks – Interactive Guide
Learn professional PyCharm features for faster Python development.
"""

def main():
    print("Welcome to Day 26 – PyCharm Tips and Tricks")
    print("Here are the most useful PyCharm features for this course.\n")

    tips = [
        ("1. Smart Code Completion", "Press Ctrl+Space (or just start typing)"),
        ("2. Refactor → Rename", "Select variable → Shift+F6 (very powerful)"),
        ("3. Live Templates", "Type 'main' then Tab → creates if __name__ == '__main__'"),
        ("4. Debug Mode", "Click left of line number to set breakpoint, then Shift+F9"),
        ("5. Run Current File", "Ctrl+Shift+F10"),
        ("6. Extract Method", "Select code → Refactor → Extract Method (Ctrl+Alt+M)"),
        ("7. Git Integration", "Built-in Git, commit, push directly from PyCharm"),
        ("8. Python Console", "Tools → Python Console (great for quick testing)"),
    ]

    for num, (title, tip) in enumerate(tips, 1):
        print(f"{num}. {title}")
        print(f"   → {tip}\n")

    print("Pro Tip: Learn these shortcuts — they will 10x your productivity!")
    print("Next: Python Object Oriented Programming (Day 27)\n")


if __name__ == "__main__":
    main()