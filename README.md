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
│   ├── day_05_maths_operations/
│   │   └── main.py 
│   ├── day_06_data_types/
│   │   └── main.py 
│   ├── day_07_converting_types/
│   │   └── main.py 
│   ├── day_08_if_else_conditionals/
│   │   └── main.py 
│   ├── day_09_logical_operations/
│   │   └── main.py 
│   ├── day_10_randomisation/
│   │   └── main.py 
│   ├── day_11_error_handling/
│   │   └── main.py 
│   ├── day_12_functions/
│   │   └── main.py 
│   ├── day_13_for_loops/
│   │   └── main.py 
│   └── day_14_code_block_indentation/   
│       └── main.py       
├── tests/                  # Comprehensive test suite (unit + integration)
│   ├── test_day_01.py
│   ├── test_day_02.py  
│   ├── test_day_03.py  
│   ├── test_day_04.py 
│   ├── test_day_05.py 
│   ├── test_day_06.py 
│   ├── test_day_07.py 
│   ├── test_day_08.py 
│   ├── test_day_09.py 
│   ├── test_day_10.py 
│   ├── test_day_11.py 
│   ├── test_day_12.py 
│   ├── test_day_13.py 
│   └── test_day_14.py
├── docs/                   # Architecture diagrams, design decisions, notes
│   └── progress/
│       ├── day-01-reflection.md      
│       ├── day-02-reflection.md    
│       ├── day-03-reflection.md  
│       ├── day-04-reflection.md 
│       ├── day-05-reflection.md
│       ├── day-06-reflection.md
│       ├── day-07-reflection.md
│       ├── day-08-reflection.md
│       ├── day-09-reflection.md
│       ├── day-10-reflection.md
│       ├── day-11-reflection.md
│       ├── day-12-reflection.md
│       ├── day-13-reflection.md
│       └── day-14-reflection.md
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

| Day | Topic                                      | Status          | Key Learnings / Deliverables                                                                                          |
|-----|--------------------------------------------|-----------------|-----------------------------------------------------------------------------------------------------------------------|
| 01  | Variables, Type Hinting & Scoping          | ✅ Completed    | Strict typing with PEP 484/695, f-strings, variable scoping rules (LEGB), local vs global vs nonlocal                  |
| 02  | String Manipulation                        | ✅ Completed    | Advanced string methods (`strip`, `title`, `upper`, `lower`, `split`, `join`, `replace`), f-string formatting & alignment, basic input cleaning |
| 03  | Input & Print Functions                    | ✅ Completed    | User input validation loops, type conversion (`int`, `float`, `str`), advanced `print` formatting (alignment, precision, `sep`, `end`), interactive console apps |
| 04  | Variable Naming Rules                      | ✅ Completed    | PEP 8 naming conventions (snake_case, CONSTANTS, private `_var`), reserved keywords, shadowing built-ins, descriptive names |
| 05  | Mathematical Operations                    | ✅ Completed    | Arithmetic operators (`+ - * / // % **`), operator precedence, floor division, modulus use cases, safe division handling |
| 06  | Built-in Data Types                        | ✅ Completed    | `int`, `float`, `bool`, `str`, `list`, `tuple`, `range`, `dict`, `set`, `frozenset`, `NoneType`, mutability vs immutability, hashability, `type()` vs `isinstance()`, `id()` |
| 07  | Converting Types (Casting)                 | ✅ Completed    | `int()`, `float()`, `str()`, `bool()`, `list()`, `tuple()`, `set()`, `dict()`, ValueError vs TypeError, safe conversion patterns |
| 08  | If / Elif / Else Conditionals              | ✅ Completed    | Comparison operators, truthy/falsy values, nested conditionals, chained `elif`, real-world decision logic               |
| 09  | Logical Operations                         | ✅ Completed    | `and`, `or`, `not`, short-circuit evaluation, combining with comparisons, truth tables, realistic combined conditions (access control, login checks) |
| 10  | Randomisation                              | ⏳ Planned      | `import random`, `random.random()`, `random.randint()`, `random.choice()`, `random.shuffle()`, seeding with `random.seed()` |
| 11  | Error Handling                             | ⏳ Planned      | `try`/`except`/`else`/`finally`, common exceptions (`ValueError`, `TypeError`, `ZeroDivisionError`, `IndexError`), custom exceptions, raising errors |
| 12  | Functions                                  | ⏳ Planned      | Defining functions, parameters vs arguments, default values, `*args`, `**kwargs`, function scope, docstrings          |
| 13  | For Loops                                  | ⏳ Planned      | Iterating over sequences (`list`, `tuple`, `str`, `range`), `for ... in ...`, `enumerate()`, `zip()`, nested loops     |
| 14  | Code Blocks and Indentation                | ⏳ Planned      | Python's indentation rules (4 spaces convention), blocks in loops/conditionals/functions, common indentation errors   |
| 15  | While Loops                                | ⏳ Planned      | `while` condition, infinite loops & break, continue, while-else clause, input validation loops                        |
| 16  | Flowchart Programming                      | ⏳ Planned      | Reading & drawing flowcharts, translating flowcharts → Python code, decision diamonds, process boxes, loops in flowcharts |
| 17  | Positional and Keyword Arguments           | ⏳ Planned      | Positional vs keyword args, required vs optional, order rules, mixing positional & keyword calls                       |
| 18  | Python Dictionaries and Lists              | ⏳ Planned      | List methods (`append`, `pop`, `remove`, `extend`, slicing), dict creation, access, update, `.get()`, `.keys()`, `.values()`, `.items()` |
| 19  | Nested Collections                         | ⏳ Planned      | Lists of lists, dicts of lists, lists of dicts, nested dicts, accessing & modifying nested structures, pretty printing |
| 20  | Returning from Functions                   | ⏳ Planned      | `return` statement, returning multiple values (tuples), early returns, implicit `None` return                         |
| 21  | Return vs. Print                           | ⏳ Planned      | Difference between printing & returning values, when to `print` vs `return`, function purity, testing returned values  |
| 22  | Docstrings vs. Comments                    | ⏳ Planned      | Writing proper docstrings (Google/Numpy style), PEP 257, difference from `#` comments, tools (help(), `__doc__`)       |
| 23  | Scope and Local/Global Variables           | ⏳ Planned      | LEGB rule, `global` keyword, `nonlocal`, avoiding global variables, closure basics                                     |
| 24  | Debugging Techniques                       | ⏳ Planned      | `print()` debugging, `pdb` / `breakpoint()`, reading tracebacks, rubber duck debugging, common bugs & patterns       |

**Beginner Projects end on Day 24**  
**Intermediate Projects start on Day 25**


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