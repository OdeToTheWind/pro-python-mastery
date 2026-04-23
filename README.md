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
│   ├── day_14_code_block_indentation/
│   │   └── main.py 
│   ├── day_15_while_loops/
│   │   └── main.py 
│   ├── day_16_flowchart_programming/
│   │   └── main.py 
│   ├── day_17_positional_keyword_arguments/
│   │   └── main.py 
│   ├── day_18_dictionaries_lists/
│   │   └── main.py 
│   ├── day_19_nested_collections/
│   │   └── main.py 
│   ├── day_20_returning_functions/
│   │   └── main.py 
│   ├── day_21_return_vs_print/
│   │   └── main.py 
│   ├── day_22_doc_string_vs_comments/
│   │   └── main.py 
│   ├── day_23_scope_local_global_variables/
│   │   └── main.py 
│   ├── day_24_debugging_techniques/
│   │   └── main.py 
│   ├── day_25_dev_env_setup_local/
│   │   └── main.py 
│   ├── day_26_pycharm_tips_tricks/
│   │   └── main.py 
│   ├── day_27_oop_basics/
│   │   └── main.py 
│   ├── day_28_classes/
│   │   └── main.py 
│   ├── day_29_external_modules/
│   │   └── main.py 
│   ├── day_30_getting_setting_attributes/
│   │   └── main.py 
│   ├── day_31_python_methods/   
│   │   └── main.py 
│   ├── day_32_class_initialisers/ 
│   │   └── main.py 
│   ├── day_33_module_aliasing/ 
│   │   └── main.py 
│   ├── day_34_optional_required_default_parameters/ 
│   │   └── main.py 
│   ├── day_35_event_listeners/
│   │   └── main.py 
│   ├── day_36_python_instances_and_state/   
│   │   └── main.py 
│   ├── day_37_python_turtle/ 
│   │   └── main.py 
│   ├── day_38_game_development_with_python_and_oop/ 
│   │   └── main.py 
│   ├── day_39_python_inheritance/ 
│   │   └── main.py 
│   └── day_40_python_slice_function/ 
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
│   ├── test_day_14.py 
│   ├── test_day_15.py 
│   ├── test_day_16.py 
│   ├── test_day_17.py 
│   ├── test_day_18.py 
│   ├── test_day_19.py 
│   ├── test_day_20.py 
│   ├── test_day_21.py 
│   ├── test_day_22.py 
│   ├── test_day_23.py 
│   ├── test_day_24.py 
│   ├── test_day_25.py 
│   ├── test_day_26.py 
│   ├── test_day_27.py 
│   ├── test_day_28.py 
│   ├── test_day_29.py 
│   ├── test_day_30.py 
│   ├── test_day_31.py 
│   ├── test_day_32.py 
│   ├── test_day_33.py 
│   ├── test_day_34.py 
│   ├── test_day_35.py 
│   ├── test_day_36.py 
│   ├── test_day_37.py 
│   ├── test_day_38.py 
│   ├── test_day_39.py 
│   └── test_day_40.py
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
│       ├── day-14-reflection.md
│       ├── day-15-reflection.md
│       ├── day-16-reflection.md
│       ├── day-17-reflection.md
│       ├── day-18-reflection.md
│       ├── day-19-reflection.md
│       ├── day-20-reflection.md
│       ├── day-21-reflection.md
│       ├── day-22-reflection.md
│       ├── day-23-reflection.md
│       ├── day-24-reflection.md
│       ├── day-25-reflection.md
│       ├── day-26-reflection.md
│       ├── day-27-reflection.md
│       ├── day-28-reflection.md
│       ├── day-29-reflection.md
│       ├── day-30-reflection.md
│       ├── day-31-reflection.md
│       ├── day-32-reflection.md
│       ├── day-33-reflection.md
│       ├── day-34-reflection.md
│       ├── day-35-reflection.md
│       ├── day-36-reflection.md
│       ├── day-37-reflection.md
│       ├── day-38-reflection.md
│       ├── day-39-reflection.md
│       └── day-40-reflection.md  
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

## Daily Progress

| Day | Topic                                              | Status             | Key Learnings / Deliverables                                                                                          |
|-----|----------------------------------------------------|--------------------|-----------------------------------------------------------------------------------------------------------------------|
| 01  | Variables, Type Hinting & Scoping                  | ✅ Completed       | Strict typing with PEP 484/695, f-strings, variable scoping rules (LEGB), local vs global vs nonlocal                  |
| 02  | String Manipulation                                | ✅ Completed       | Advanced string methods (`strip`, `title`, `upper`, `lower`, `split`, `join`, `replace`), f-string formatting & alignment, basic input cleaning |
| 03  | Input & Print Functions                            | ✅ Completed       | User input validation loops, type conversion (`int`, `float`, `str`), advanced `print` formatting, interactive console apps |
| 04  | Variable Naming Rules                              | ✅ Completed       | PEP 8 naming conventions (snake_case, CONSTANTS, private `_var`), reserved keywords, descriptive names                 |
| 05  | Mathematical Operations                            | ✅ Completed       | Arithmetic operators (`+ - * / // % **`), operator precedence, floor division, safe division handling                 |
| 06  | Built-in Data Types                                | ✅ Completed       | `int`, `float`, `bool`, `str`, `list`, `tuple`, `dict`, `set`, mutability vs immutability, hashability, `type()` vs `isinstance()` |
| 07  | Converting Types (Casting)                         | ✅ Completed       | `int()`, `float()`, `str()`, `bool()`, `list()`, `tuple()`, `set()`, `dict()`, ValueError vs TypeError                |
| 08  | If / Elif / Else Conditionals                      | ✅ Completed       | Comparison operators, truthy/falsy values, nested conditionals, chained `elif`                                        |
| 09  | Logical Operations                                 | ✅ Completed       | `and`, `or`, `not`, short-circuit evaluation, combining with comparisons, truth tables, access control examples       |
| 10  | Randomisation                                      | ✅ Completed       | `random` module, `randint()`, `choice()`, `shuffle()`, `seed()`, password generator, games                           |
| 11  | Error Handling                                     | ✅ Completed       | `try`/`except`/`else`/`finally`, common exceptions (`ValueError`, `TypeError`, `ZeroDivisionError`, `KeyError`)     |
| 12  | Functions                                          | ✅ Completed       | Parameters, default arguments, `*args`, `**kwargs`, docstrings, type hints                                            |
| 13  | For Loops                                          | ✅ Completed       | `for` loops, `range()`, `enumerate()`, `zip()`, nested loops, multiplication tables                                   |
| 14  | Code Blocks and Indentation                        | ✅ Completed       | Python's indentation rules (4 spaces), blocks in loops/conditionals/functions, common IndentationError                 |
| 15  | While Loops                                        | ✅ Completed       | `while` loops, `break`, `continue`, `while-else`, input validation, guessing games                                    |
| 16  | Flowchart Programming                              | ✅ Completed       | Reading flowcharts, converting decision diamonds to `if-elif-else`, loops in flowcharts                               |
| 17  | Positional and Keyword Arguments                   | ✅ Completed       | Positional vs keyword args, default values, `*args`, `**kwargs`, function flexibility                                |
| 18  | Python Dictionaries and Lists                      | ✅ Completed       | List methods (`append`, `pop`, `sort`), dict methods (`.get()`, `.update()`, `.items()`), shopping cart & inventory  |
| 19  | Nested Collections                                 | ✅ Completed       | List of dicts, dict of lists, list of lists, dict of dicts, classroom management system                              |
| 20  | Returning Functions                                | ✅ Completed       | `return` statement, returning multiple values, early returns, return vs print                                        |
| 21  | Return vs. Print                                   | ✅ Completed       | Difference between printing and returning data, reusability, function composition                                    |
| 22  | Docstrings vs. Comments                            | ✅ Completed       | `#` comments vs `"""` docstrings, Google-style docstrings, `__doc__` attribute                                       |
| 23  | Scope and Local/Global Variables                   | ✅ Completed       | LEGB rule, `global` keyword, `nonlocal`, why globals are dangerous                                                    |
| 24  | Debugging Techniques                               | ✅ Completed       | Print debugging, reading tracebacks, common bugs, `breakpoint()`, rubber duck debugging                              |

### Intermediate Python (Day 25 onwards)

| Day | Topic                                              | Status             | Key Learnings / Deliverables                                                                                          |
|-----|----------------------------------------------------|--------------------|-----------------------------------------------------------------------------------------------------------------------|
| 25  | Local Development Environment Setup | ✅ Completed       | Setting up virtual environments, project structure, best practices for local development                             |
| 26  | PyCharm Tips and Tricks                            | ✅ Completed       | Advanced IDE features, debugging in PyCharm, refactoring tools, live templates                                        |
| 27  | Python Object Oriented Programming                 | ✅ Completed       | OOP concepts: classes, objects, encapsulation, abstraction                                                            |
| 28  | Creating Classes in Python                         | ✅ Completed       | Defining classes, `__init__`, attributes, methods                                                                     |
| 29  | Using External Python Modules / Import             | ✅ Completed       | `import`, `from ... import`, installing packages with pip, virtual environments                                      |
| 30  | Getting / Setting Attributes                       | ✅ Completed       | `@property`, getters and setters, attribute access control                                                            |
| 31  | Python Methods                                     | ✅ Completed       | Instance methods, class methods (`@classmethod`), static methods (`@staticmethod`)                                   |
| 32  | Class Initialisers                                 | ✅ Completed       | `__init__` constructor, default values, validation in constructors                                                    |
| 33  | Module Aliasing                                    | ✅ Completed       | `import module as alias`, organizing large codebases                                                                  |
| 34  | Optional, Required and Default Parameters          | ✅ Completed       | Advanced function parameters, `*args`, `**kwargs`, parameter ordering rules                                           |
| 35  | Event Listeners                                    | ✅ Completed       | Event-driven programming concepts, callbacks                                                                          |
| 36  | Python Instances and State                         | ✅ Completed       | Instance variables, maintaining state in objects                                                                      |
| 37  | Python Turtle                                      | ✅ Completed       | Graphics with Turtle module, drawing shapes and animations                                                            |
| 38  | Game Development with Python and OOP               | ✅ Completed       | Building simple games using OOP principles                                                                            |
| 39  | Python Inheritance                                 | ✅ Completed       | Single and multiple inheritance, `super()`, method overriding                                                         |
| 40  | Python Slice Function                              | ✅ Completed       | Advanced slicing techniques for lists and strings                                                                     |
| 41  | File I/O - Reading and Writing to Local Files      | ⏳ Planned        | `open()`, context managers (`with`), reading/writing text files                                                       |
| 42  | File Directories                                   | ⏳ Planned        | `os` and `pathlib` modules, working with folders and paths                                                            |
| 43  | Reading and Writing to CSV                         | ⏳ Planned        | CSV module, reading/writing tabular data                                                                              |
| 44  | Introduction to the Pandas Framework               | ⏳ Planned        | DataFrames, basic data analysis with pandas                                                                           |
| 45  | List Comprehensions                                | ⏳ Planned        | Concise list creation, filtering, and transformation                                                                  |
| 46  | Dictionary Comprehensions                          | ⏳ Planned        | Creating dictionaries using comprehension syntax                                                                      |
| 47  | Packing and Unpacking Functions in Python          | ⏳ Planned        | Advanced argument unpacking with `*` and `**`                                                                         |
| 48  | Creating Desktop GUI Apps with Tkinter             | ⏳ Planned        | Building graphical user interfaces with Tkinter                                                                       |
| 49  | Strongly Dynamic Typing                            | ⏳ Planned        | Python's dynamic typing behavior and implications                                                                     |
| 50  | Error Handling and Exceptions                      | ⏳ Planned        | Advanced exception handling patterns                                                                                  |
| 51  | Try / Except / Raise                               | ⏳ Planned        | Raising custom exceptions, exception hierarchies                                                                      |
| 52  | Working with JSONs                                 | ⏳ Planned        | `json` module, serialization and deserialization                                                                      |
| 53  | Local Persistence                                  | ⏳ Planned        | Saving and loading application state                                                                                  |
| 54  | Sending Email with Python and SMTP                 | ⏳ Planned        | Automating emails using `smtplib`                                                                                     |
| 55  | Working with Date and Time                         | ⏳ Planned        | `datetime` module, date calculations and formatting                                                                   |
| 56  | Hosting Python Code Online with PythonAnywhere     | ⏳ Planned        | Deploying Python applications to the cloud                                                                            |

**Phase 1: Beginner Fundamentals (Days 1–24) — Completed! 🎓**  
**Phase 2: Intermediate Projects start from Day 25**

---

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
