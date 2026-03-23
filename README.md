# Pro Python Mastery: 100-Day Engineering Challenge

[![Python CI](https://github.com/OdeToTheWind/pro-python-mastery/actions/workflows/python-tests.yml/badge.svg)](https://github.com/OdeToTheWind/pro-python-mastery/actions)
![Python Version](https://img.shields.io/badge/python-3.12–3.14-blue)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Overview

This repository documents a structured 100-day professional development challenge focused on advanced Python software engineering practices. With over four years of development experience, the goal is to demonstrate production-grade code quality through:

- Strict static typing with modern type hints  
- Test-Driven Development (TDD) with ≥80% test coverage  
- Clean, modular architecture and design patterns  
- Automated testing and continuous integration via GitHub Actions  
- Adoption of the latest Python language features (3.12–3.14)

This project is part of a broader 10-repository portfolio showcasing technical depth, system design thinking, and disciplined engineering habits.

## Project Structure

The repository is organized as a Python package with clear separation of concerns:
```text
pro-python-mastery/
├── .github/                # GitHub Actions CI/CD pipelines
│   └── workflows/
│       └── python-tests.yml
├── src/                    # Production code – modular by day/topic
│   ├── day_01_variables/
│   │   └── main.py
│   ├── day_02_strings/
│   │   └── main.py  
│   ├── day_03_input_output/
│   │   └── main.py  
│   ├── day_04_variable_name_rules/
│   │   └── main.py  
│   └── day_04_maths_operations/  
│       └── main.py       
├── tests/                  # Comprehensive test suite (unit + integration)
│   ├── test_day_01.py
│   ├── test_day_02.py  
│   ├── test_day_03.py  
│   ├── test_day_04.py 
│   └── test_day_05.py
├── docs/                   # Architecture diagrams, design decisions, notes
│   └── progress/
│       ├── day-01-reflection.md      
│       ├── day-02-reflection.md    
│       ├── day-03-reflection.md  
│       ├── day-04-reflection.md
│       └── day-05-reflection.md
├── propython.sh            # Executable file for the Repo
├── requirements.txt        # Development and testing dependencies
├── README.md
└── LICENSE
```

## Key Engineering Practices

- **Type Safety** — Full use of the `typing` module, type hints in function signatures, and exploration of modern features (PEP 484, 563, 695)  
- **Testing** — Rigorous TDD workflow using `pytest`, with unit tests for each daily challenge  
- **CI/CD** — Automated testing via GitHub Actions (linting, type checking with mypy, and test runs planned on every push)  
- **Modern Python** — Leveraging syntax, formatting, and best practices from Python 3.12–3.14 (f-strings, type hints, structural pattern matching where applicable)

## Daily Progress

| Day | Topic                              | Status       | Key Learnings / Deliverables                                      |
|-----|------------------------------------|--------------|-------------------------------------------------------------------|
| 01  | Variables, Type Hinting & Scoping  | ✅ Completed | Strict typing with PEP 484/695, f-strings, variable scoping rules |
| 02  | String Manipulation                | ✅ Completed | Advanced string methods (strip, title, upper), f-string formatting & alignment, basic input cleaning |
| 03  | Input & Print Functions            | ✅ In Progress | User input validation, type conversion, advanced print formatting (alignment, precision), interactive console apps |
| 04  | Variable Naming Rules             | ⏳ Planning  |-------------------------------------------------------------------|
| ... | ...                                | ...          | ...                                                               |

Daily reflections, code explanations, and design decisions are available in [docs/progress/](./docs/progress/)

## Getting Started

### Prerequisites

- Python 3.12 or newer (recommended: 3.14 for latest features)
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/OdeToTheWind/pro-python-mastery.git
cd pro-python-mastery

# (Recommended) Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate    # Linux/macOS/Git Bash
# or
.venv\Scripts\activate       # Windows Command Prompt
# or
.venv\Scripts\Activate.ps1   # Windows PowerShell

# Install development dependencies
pip install -r requirements.txt
```

### RUNNING TEST 
```bash
# Run the full test suite
pytest

# With coverage report
pytest --cov=src --cov-report=html
# Open htmlcov/index.html in your browser
```

### Linting & Type Checking
```bash
# Run mypy static type checker
mypy src tests

# Run ruff (linting + formatting check)
ruff check .
ruff format --check .
```

## Contributing

This is a personal challenge repository, but issues, suggestions, and thoughtful discussions are welcome.

## License

MIT License – see the LICENSE file for details.

### Main Improvements Made
- Removed casual emojis from headings (kept only where they add value)
- Professional tone and phrasing
- Clearer structure and language
- Added realistic setup instructions (venv activation for all major shells)
- Included linting/type-checking commands (common in pro Python repos)
- Better table formatting & future-proof columns
- Removed redundant repetition in the overview

Feel free to copy-paste this directly into your `README.md`.  

If you'd like to add badges for coverage, mypy, ruff, or a progress percentage,let me know — I can help generate those too. Good luck with the rest of the 100 days! 🚀 