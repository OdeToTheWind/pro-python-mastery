# src/day_25_dev_env_setup_local/main.py
"""
Day 25: Local Development Environment Setup – Interactive Checker
"""

import sys
import os

def main():
    print("Welcome to Day 25 – Local Development Environment Setup")
    print("Let's verify your Python development environment.\n")

    print(f"Python Version: {sys.version.split()[0]}")
    if sys.version_info >= (3, 8):
        print("✅ Python version is good (>= 3.8)")
    else:
        print("⚠️  Consider upgrading to Python 3.10+")

    print("\nVirtual Environment Check:")
    if 'VIRTUAL_ENV' in os.environ:
        print(f"✅ Inside virtual environment: {os.environ['VIRTUAL_ENV']}")
    else:
        print("⚠️  Not inside a virtual environment")
        print("   Tip: python -m venv .venv && source .venv/bin/activate (or activate.bat on Windows)")

    print("\nRecommended Project Structure:")
    print("pro-python-mastery/")
    print("├── src/")
    print("├── tests/")
    print("├── .venv/          ← gitignored")
    print("├── requirements.txt")
    print("├── README.md")
    print("└── .gitignore")

    print("\nNext Steps:")
    print("1. Create virtual environment: python -m venv .venv")
    print("2. Activate it")
    print("3. pip install -r requirements.txt")
    print("4. Use consistent 4-space indentation")

    print("\nYour environment is ready for Intermediate Projects!")
    print("Next: PyCharm Tips and Tricks (Day 26)\n")


if __name__ == "__main__":
    main()