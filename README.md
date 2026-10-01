<p align="center">
  <img src="docs/assets/banner.svg" alt="Pro Python Mastery – 100 days from your first variable to production-ready Python" width="100%">
</p>

<h1 align="center">Pro Python Mastery – 100 Days of Professional Python</h1>

<p align="center">
  <a href="https://github.com/OdeToTheWind/pro-python-mastery/actions/workflows/python-tests.yml"><img src="https://github.com/OdeToTheWind/pro-python-mastery/actions/workflows/python-tests.yml/badge.svg" alt="CI status"></a>
  <img src="https://img.shields.io/badge/python-3.12%20%7C%203.13%20%7C%203.14-3776ab?style=flat-square" alt="Python 3.12, 3.13, 3.14">
  <img src="https://img.shields.io/badge/days-100%20%2F%20100-2ea44f?style=flat-square" alt="100 of 100 days">
  <img src="https://img.shields.io/badge/coverage%20gate-85%25-2ea44f?style=flat-square" alt="Coverage gate 85%">
  <a href="LICENSE"><img src="https://img.shields.io/badge/code-MIT-1a1a1a?style=flat-square" alt="Code: MIT"></a>
  <a href="LICENSE-CONTENT"><img src="https://img.shields.io/badge/content-CC%20BY%204.0-1a1a1a?style=flat-square" alt="Content: CC BY 4.0"></a>
</p>

**Pro Python Mastery** is a free, open course that takes you from your first variable to
production-ready Python in 100 days. Each day is a small, realistic project. Day 1 is a
learning-streak tracker, Day 47 is a GPS route planner and Day 100 is an expense tracker
you could put on your CV. Every day ships three pieces that CI keeps in agreement: typed,
documented **code** with a runnable demo, a **test suite** that doubles as worked examples,
and a **reflection** that records what was learned and which mistakes to avoid. Nothing
in the progress table below is self-reported. If a day's code, tests or reflection go
missing or out of date, the build fails.

```bash
git clone https://github.com/OdeToTheWind/pro-python-mastery.git && cd pro-python-mastery
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
python -m src.day_01_variables.main                    # run your first day
```

---

## Project Goals

The course is built around five objectives. Each one is backed by something in the
repository that can be checked, so none of them is only a promise.

| # | Objective | How the repository delivers it |
|:-:|---|---|
| 1 | **Teach Python the way it is written professionally.** | Every module is type-hinted, documented, linted with ruff and type-checked with mypy, from Day 1 onwards. |
| 2 | **Learn by building, not by reading.** | 100 distinct scenarios, one per day. No two days share a project, and CI enforces that. |
| 3 | **Make testing a habit, not a chapter.** | Every day has its own pytest suite, at least 5 tests each, with no network access and no placeholder assertions. |
| 4 | **Keep the course honest and current.** | `tests/test_syllabus_sync.py` ties the syllabus, code, tests, reflections and this README together. |
| 5 | **Finish with portfolio-grade work.** | Phase 5 (Days 83–100) builds complete tools: CLIs, services, pipelines, packaging and a multi-module capstone. |

### How to use each day

1. **Read the scenario** at the top of `src/day_XX_<topic>/main.py`, and the `DELIVERABLES` map below it.
2. **Run the demo:** `python -m src.day_XX_<topic>.main`.
3. **Read the tests** in `tests/test_day_XX.py`. They show the edge cases that matter.
4. **Break something on purpose** and watch a test fail, then fix it.
5. **Read the reflection** in `docs/progress/day-XX-reflection.md` for the pitfalls and the next step.

---

## Tech Stack & Tools Overview

### Language and runtime

| Tool | Role in this project |
|---|---|
| **Python 3.12+** | The language taught. Modern syntax throughout: PEP 695 generics, `match`, `ExceptionGroup` and `tomllib`. |
| **Standard library** | Most days use only the standard library: `pathlib`, `dataclasses`, `asyncio`, `sqlite3`, `concurrent.futures`, `logging`, `argparse`, `re` and more. |

### Quality and automation

| Tool | Role in this project |
|---|---|
| **pytest** + **pytest-cov** | Test runner and coverage measurement, with a coverage gate in CI. |
| **ruff** | Linting and import sorting (rule sets `E F W B I UP SIM`). |
| **mypy** | Static type checking of every day module. |
| **GitHub Actions** | CI on Python 3.12, 3.13 and 3.14 (Linux), plus Windows and macOS. |
| **`propython.sh`** | One local command that runs exactly what CI runs. |
| **build** · **hatchling** · **twine** | Building and checking real wheels and source distributions (Days 79 and 96). |

### Libraries used by specific days

| Library | Used for (days) |
|---|---|
| **requests** | HTTP clients and polite scraping (58–60, 62, 97) |
| **aiohttp** | Concurrent async HTTP and local test servers (76, 85) |
| **beautifulsoup4** | HTML parsing (62, 97) |
| **selenium** | Browser automation (63) |
| **pandas** | DataFrames (44) |
| **numpy** | Vectorised computation and simulation (95, 98) |
| **schedule** | Job scheduling (89, 97) |
| **PyYAML** · **python-dotenv** | YAML configuration (77) and secrets from `.env` (60, 91) |
| **memory-profiler** · **tzdata** · **packaging** | Memory profiling (80), time zones on Windows (55) and requirement parsing (29) |

---

## Dataset Description

This course does not depend on one large dataset. Instead, each day brings the small,
purpose-built data its scenario needs. The data falls into four groups, and none of it
contains personal information.

| Source | Where it comes from | Used by |
|---|---|---|
| **Synthetic in-code data** | Small, readable samples written directly in each module, for example orders, sensor readings, ticket texts and patient-intake forms. Edge cases are deliberately included: bad rows, duplicates, out-of-range values and malformed input. | Most days |
| **Seeded generators** | Larger data produced reproducibly from a fixed random seed, so every run and every test sees the same values. Examples are FASTQ reads (Day 90), city coordinates (Day 95) and epidemic runs (Day 98). | 90, 95, 98 and others |
| **Local test servers** | Fake websites, APIs and webhooks started on `127.0.0.1` during tests and demos (aiohttp, `http.server`, raw `asyncio`). They make network code testable without the internet. | 76, 85, 93, 97 |
| **Public practice services** | Sites built for learning: [quotes.toscrape.com](https://quotes.toscrape.com), [JSONPlaceholder](https://jsonplaceholder.typicode.com) and [httpbin](https://httpbin.org). These are contacted **only** when a demo is run by hand, never in tests. | 58, 59, 62, 63 |

All generated files are written to temporary directories, and tests are confined to
pytest's `tmp_path`. Credentials for the e-mail, API and SMS days (54, 60, 61) are read
from environment variables. Copy [`.env.example`](.env.example) to a git-ignored `.env` to try
them for real.

---

## Project Directory & Structure

```text
pro-python-mastery/
├── src/                              # one package per day: the lessons
│   ├── day_01_variables/
│   │   ├── __init__.py
│   │   └── main.py                   # "Scenario:" docstring · DELIVERABLES · functions · main()
│   ├── …                             # days 02–99
│   └── day_100_portfolio_capstone/   # multi-module capstone package (budgetly)
├── tests/
│   ├── conftest.py                   # shared fixtures
│   ├── test_day_01.py … test_day_100.py
│   └── test_syllabus_sync.py         # keeps syllabus, code, tests, docs and README in agreement
├── docs/
│   ├── assets/banner.svg
│   └── progress/
│       ├── notes/day-XX.json         # hand-written learnings, pitfalls, next step
│       └── day-XX-reflection.md      # generated from notes + code
├── scripts/build_reflections.py      # generates reflections and the README's tables
├── .github/                          # CI workflow, issue and pull request templates
├── syllabus.md                       # the 100-day curriculum, grouped into five phases
├── learning_develop.md               # the plan for the course after Day 100
├── propython.sh                      # local quality gate (same checks as CI)
├── pyproject.toml                    # pytest, coverage, ruff and mypy configuration
├── requirements.txt / requirements-dev.txt
├── CONTRIBUTING.md · CODE_OF_CONDUCT.md · SECURITY.md · CITATION.cff
└── LICENSE (MIT, code) · LICENSE-CONTENT (CC BY 4.0, course text)
```

---

## System & Data Architecture

The repository is a small system with one source of truth for each fact. Hand-written
inputs are on the left. Everything on the right is generated or verified from them, so
nothing can drift.

```mermaid
%%{init: {'theme':'base','themeVariables':{'primaryColor':'#f6f8fa','primaryTextColor':'#1f2328','primaryBorderColor':'#3776ab','lineColor':'#3776ab','fontSize':'13px'}}}%%
flowchart LR
  subgraph authored ["Written by authors"]
    S["syllabus.md<br/><sub>topics · deliverables · status</sub>"]
    C["src/day_XX/main.py<br/><sub>scenario · DELIVERABLES · code</sub>"]
    T["tests/test_day_XX.py<br/><sub>behaviour + edge cases</sub>"]
    N["notes/day-XX.json<br/><sub>learnings · pitfalls</sub>"]
  end
  subgraph generated ["Generated"]
    R["day-XX-reflection.md"]
    I["README tables<br/><sub>KPIs · progress · index</sub>"]
  end
  S & C & T & N --> B["scripts/build_reflections.py"]
  B --> R & I
  G{{"CI · test_syllabus_sync.py"}} -. "fails the build if anything is stale" .-> generated
```

Each day, in turn, follows the same internal shape:

```mermaid
%%{init: {'theme':'base','themeVariables':{'primaryColor':'#f6f8fa','primaryTextColor':'#1f2328','primaryBorderColor':'#3776ab','lineColor':'#3776ab','fontSize':'13px'}}}%%
flowchart LR
  A["SCENARIO<br/><sub>a realistic problem</sub>"] --> B["DELIVERABLES<br/><sub>skill → code map</sub>"]
  B --> C["CODE<br/><sub>typed functions</sub>"]
  C --> D["DEMO<br/><sub>python -m … main</sub>"]
  C --> E["TESTS<br/><sub>pytest, no network</sub>"]
  E --> F["REFLECTION<br/><sub>learnings · pitfalls · next</sub>"]
```

---

## Key Performance Indicators & Metrics

These numbers are **measured from the repository** by `scripts/build_reflections.py`, and CI
fails if they are out of date.

<!-- kpis:start -->
- **Curriculum completion:** 100 / 100 days covered, each with code, tests and a reflection.
- **Test functions:** 974 across 100 test modules (parametrised cases run more).
- **Deliverables mapped to code:** 646 `DELIVERABLES` entries, each checked to resolve.
- **Source size:** 12,258 non-blank lines of Python in `src/`.
- **Coverage gate:** CI fails below 85 % coverage (lines and branches).
- **Python versions in CI:** 3.12, 3.13, 3.14.
- **Operating systems in CI:** macOS, Linux, Windows.
- **Quality checks per commit:** ruff lint · mypy type-check · pytest with coverage · syllabus sync.
<!-- kpis:end -->

---

## Project Report & Progress Tracker

<!-- phase-status:start -->
| Phase | Days | Status |
|---|:-:|---|
| 1 · Beginner Fundamentals | 1–24 | ✅ Complete (24/24) |
| 2 · Intermediate Python | 25–56 | ✅ Complete (32/32) |
| 3 · API Clients, Automation & Data Acquisition | 57–63 | ✅ Complete (7/7) |
| 4 · Advanced Python Language & Tooling | 64–82 | ✅ Complete (19/19) |
| 5 · Capstone-Style Pure-Python Projects | 83–100 | ✅ Complete (18/18) |
<!-- phase-status:end -->

<details>
<summary><b>Full 100-day course index</b> (scenario and links for every day)</summary>

Level: 🟢 Beginner · 🟡 Intermediate · 🟠 Advanced · 🔴 Capstone

<!-- course-index:start -->
| Day | Topic | Level | Scenario you build | Links |
|---:|---|:-:|---|---|
| 1 | Variables, Type Hinting & Scoping | 🟢 | A *learning-streak tracker* that records study sessions. | [code](src/day_01_variables/main.py) · [tests](tests/test_day_01.py) · [notes](docs/progress/day-01-reflection.md) |
| 2 | String Manipulation | 🟢 | A *conference badge printer* that turns messy sign-up data into clean, aligned badges. | [code](src/day_02_strings/main.py) · [tests](tests/test_day_02.py) · [notes](docs/progress/day-02-reflection.md) |
| 3 | Input & Print Functions | 🟢 | A *workshop registration desk* that asks attendees questions in the console, validates every answer and prints a receipt. | [code](src/day_03_input_output/main.py) · [tests](tests/test_day_03.py) · [notes](docs/progress/day-03-reflection.md) |
| 4 | Variable Naming Rules | 🟢 | A *code-review bot* that inspects proposed variable names and gives the author syntax errors (must fix) and PEP 8 style warnings (should fix). | [code](src/day_04_variable_name_rules/main.py) · [tests](tests/test_day_04.py) · [notes](docs/progress/day-04-reflection.md) |
| 5 | Mathematical Operations | 🟢 | A *restaurant bill splitter* – arithmetic with money, where rounding, floor division and division by zero all matter. | [code](src/day_05_math_operations/main.py) · [tests](tests/test_day_05.py) · [notes](docs/progress/day-05-reflection.md) |
| 6 | Built-in Data Types | 🟢 | A *value inspector* – paste any Python literal and get a report on its type, category, mutability, hashability and size. | [code](src/day_06_data_types/main.py) · [tests](tests/test_day_06.py) · [notes](docs/progress/day-06-reflection.md) |
| 7 | Converting Types (Casting) | 🟢 | A *spreadsheet import cleaner* – every cell arrives as text and must be cast to the right Python type, with precise error reporting. | [code](src/day_07_converting_types/main.py) · [tests](tests/test_day_07.py) · [notes](docs/progress/day-07-reflection.md) |
| 8 | If / Elif / Else Conditionals | 🟢 | A *hiking-trip weather advisor* that decides what to pack and whether the hike is safe. | [code](src/day_08_if_else_conditionals/main.py) · [tests](tests/test_day_08.py) · [notes](docs/progress/day-08-reflection.md) |
| 9 | Logical Operations | 🟢 | An *office building access controller* deciding who may open which door, and a tracer that proves when Python stops evaluating. | [code](src/day_09_logical_operations/main.py) · [tests](tests/test_day_09.py) · [notes](docs/progress/day-09-reflection.md) |
| 10 | Randomisation | 🟢 | A *board-game night toolkit* – dice, a card deck, a raffle and a password generator for the Wi-Fi. | [code](src/day_10_randomisation/main.py) · [tests](tests/test_day_10.py) · [notes](docs/progress/day-10-reflection.md) |
| 11 | Error Handling | 🟢 | A *greenhouse sensor log reader* – log files are messy, devices disappear and humans type bad values. The program must keep going. | [code](src/day_11_error_handling/main.py) · [tests](tests/test_day_11.py) · [notes](docs/progress/day-11-reflection.md) |
| 12 | Functions | 🟢 | A *coffee-shop ordering system* built from small, documented, type-hinted functions. | [code](src/day_12_functions/main.py) · [tests](tests/test_day_12.py) · [notes](docs/progress/day-12-reflection.md) |
| 13 | For Loops | 🟢 | A *school sports-day results board* – iterate over athletes, lanes and heats to build tables and rankings. | [code](src/day_13_for_loops/main.py) · [tests](tests/test_day_13.py) · [notes](docs/progress/day-13-reflection.md) |
| 14 | Code Blocks and Indentation | 🟢 | A *snippet linter for a coding bootcamp* – students paste code and the tool compiles it, explains indentation errors and offers an automatic fix. | [code](src/day_14_code_block_indentation/main.py) · [tests](tests/test_day_14.py) · [notes](docs/progress/day-14-reflection.md) |
| 15 | While Loops | 🟢 | An *arcade cabinet* – a number-guessing game, a PIN lock and a coin-counting machine, each driven by ``while`` loops. | [code](src/day_15_while_loops/main.py) · [tests](tests/test_day_15.py) · [notes](docs/progress/day-15-reflection.md) |
| 16 | Flowchart Programming | 🟢 | A *public library desk* – loan approvals, overdue fines and a returns-sorting conveyor, each first drawn as a flowchart and then translated into Python. | [code](src/day_16_flowchart_programming/main.py) · [tests](tests/test_day_16.py) · [notes](docs/progress/day-16-reflection.md) |
| 17 | Positional and Keyword Arguments | 🟢 | An *airline booking API* where some arguments must be positional (route), some must be named (cabin, flexibility) and some are optional. | [code](src/day_17_positional_keyword_arguments/main.py) · [tests](tests/test_day_17.py) · [notes](docs/progress/day-17-reflection.md) |
| 18 | Python Dictionaries and Lists | 🟢 | A *neighbourhood grocery store* – a dict-based inventory behind the counter and a list-based shopping cart in front of it. | [code](src/day_18_dictionaries_lists/main.py) · [tests](tests/test_day_18.py) · [notes](docs/progress/day-18-reflection.md) |
| 19 | Nested Collections | 🟢 | A *school gradebook* – classes contain students, students contain subjects, subjects contain lists of scores. | [code](src/day_19_nested_collections/main.py) · [tests](tests/test_day_19.py) · [notes](docs/progress/day-19-reflection.md) |
| 20 | Returning Functions | 🟢 | A *blog post analyser* – functions that return values, multiple values, exit early on bad input, return other functions and compose into a text-processing pipeline. | [code](src/day_20_returning_functions/main.py) · [tests](tests/test_day_20.py) · [notes](docs/progress/day-20-reflection.md) |
| 21 | Return vs. Print | 🟢 | A *freelancer invoicing tool* – the same calculations written two ways (print-only vs return) to show why returning data is the reusable design. | [code](src/day_21_return_vs_print/main.py) · [tests](tests/test_day_21.py) · [notes](docs/progress/day-21-reflection.md) |
| 22 | Docstrings vs. Comments | 🟢 | A *kitchen unit-conversion library* that is documented properly and a documentation auditor that inspects it. | [code](src/day_22_doc_string_vs_comments/main.py) · [tests](tests/test_day_22.py) · [notes](docs/progress/day-22-reflection.md) |
| 23 | Scope and Local/Global Variables | 🟢 | A *web-app feature-flag service*. Configuration lives at module level, request handlers have their own locals and rate limiters are closures. | [code](src/day_23_scope_local_global_variables/main.py) · [tests](tests/test_day_23.py) · [notes](docs/progress/day-23-reflection.md) |
| 24 | Debugging Techniques | 🟢 | A *payroll script* that ships with a real bug. We find it with print debugging, read its traceback, set a (switchable) breakpoint, and locate the first failing input systematically. | [code](src/day_24_debugging_techniques/main.py) · [tests](tests/test_day_24.py) · [notes](docs/progress/day-24-reflection.md) |
| 25 | Local Development Environment Setup | 🟡 | A *project doctor* that inspects a checkout (this repository by default) and reports whether the local environment follows best practice. | [code](src/day_25_dev_env_setup_local/main.py) · [tests](tests/test_day_25.py) · [notes](docs/progress/day-25-reflection.md) |
| 26 | PyCharm Tips and Tricks | 🟡 | A *pocket IDE coach* – a searchable shortcut cheat-sheet per OS, a live-template expander and a safe "Rename" refactoring that works the way the IDE's does (on tokens, not on raw text). | [code](src/day_26_pycharm_tips_tricks/main.py) · [tests](tests/test_day_26.py) · [notes](docs/progress/day-26-reflection.md) |
| 27 | Python Object Oriented Programming | 🟡 | A *payment gateway* that accepts several payment methods through one abstract interface while hiding sensitive card data. | [code](src/day_27_oop_basics/main.py) · [tests](tests/test_day_27.py) · [notes](docs/progress/day-27-reflection.md) |
| 28 | Creating Classes in Python | 🟡 | A *community library catalogue* – a ``Book`` class with an initialiser, instance attributes, behaviour methods and friendly dunders. | [code](src/day_28_classes/main.py) · [tests](tests/test_day_28.py) · [notes](docs/progress/day-28-reflection.md) |
| 29 | Using External Python Modules / Import | 🟡 | A *dependency inspector* for this course – it checks which third-party packages are installed, reads their versions, uses one of them (``requests``) offline, and organises its own helpers as a local package. | [code](src/day_29_external_modules/main.py) · [tests](tests/test_day_29.py) · [notes](docs/progress/day-29-reflection.md) |
| 30 | Getting / Setting Attributes | 🟡 | A *smart thermostat* whose temperature can be read and written in Celsius or Fahrenheit, but never set to an unsafe value. | [code](src/day_30_getting_setting_attributes/main.py) · [tests](tests/test_day_30.py) · [notes](docs/progress/day-30-reflection.md) |
| 31 | Python Methods | 🟡 | A *pizzeria ordering system* where each kind of method has a clear job: instance methods change one pizza, class methods build pizzas or change shop-wide settings, static methods are utilities that need neither. | [code](src/day_31_python_methods/main.py) · [tests](tests/test_day_31.py) · [notes](docs/progress/day-31-reflection.md) |
| 32 | Class Initialisers | 🟡 | *opening bank accounts* – the constructor is the gatekeeper that guarantees every account object is valid from the first moment it exists. | [code](src/day_32_class_initialisers/main.py) · [tests](tests/test_day_32.py) · [notes](docs/progress/day-32-reflection.md) |
| 33 | Module Aliasing | 🟡 | A *fitness-tracker weekly summary* that needs two different ``loads`` functions and some long module names – aliasing keeps it readable. | [code](src/day_33_module_aliasing/main.py) · [tests](tests/test_day_33.py) · [notes](docs/progress/day-33-reflection.md) |
| 34 | Optional, Required and Default Parameters | 🟡 | A *CI job scheduler* whose ``schedule_job`` signature uses every parameter kind Python offers, in the only order Python allows. | [code](src/day_34_optional_required_default_parameters/main.py) · [tests](tests/test_day_34.py) · [notes](docs/progress/day-34-reflection.md) |
| 35 | Event Listeners | 🟡 | A *smart-home hub*. Devices emit events (doorbell rang, motion detected); any number of independent listeners react without the devices knowing who is listening. | [code](src/day_35_event_listeners/main.py) · [tests](tests/test_day_35.py) · [notes](docs/progress/day-35-reflection.md) |
| 36 | Python Instances and State | 🟡 | *food-delivery orders*. Every order object tracks its own state as it moves through a lifecycle (placed → cooking → out for delivery → delivered, or cancelled), records history, and releases resources when it closes. | [code](src/day_36_python_instances_and_state/main.py) · [tests](tests/test_day_36.py) · [notes](docs/progress/day-36-reflection.md) |
| 37 | Python Turtle | 🟡 | A *greeting-card artist* – draws shapes, a star burst, a spiral and an animated orbit with ``turtle``. | [code](src/day_37_python_turtle/main.py) · [tests](tests/test_day_37.py) · [notes](docs/progress/day-37-reflection.md) |
| 38 | Game Development with Python and OOP | 🟡 | *Dungeon Duel* – a turn-based battle between a hero and monsters. Both sides attack, the hero can heal with limited potions, and the battle can be won **or lost**. Randomness is injected so games are reproducible in tests. | [code](src/day_38_game_development_with_python_and_oop/main.py) · [tests](tests/test_day_38.py) · [notes](docs/progress/day-38-reflection.md) |
| 39 | Python Inheritance | 🟡 | A *smart-device product line*. A base ``Device`` is specialised by single inheritance (``Camera``) and combined with capability mixins through multiple inheritance (``SmartDoorbell``) using cooperative ``super()``. | [code](src/day_39_python_inheritance/main.py) · [tests](tests/test_day_39.py) · [notes](docs/progress/day-39-reflection.md) |
| 40 | Python Slice Function | 🟡 | A *bank-statement parser* for fixed-width text records, plus a playlist editor – both lean on slicing. | [code](src/day_40_python_slice_function/main.py) · [tests](tests/test_day_40.py) · [notes](docs/progress/day-40-reflection.md) |
| 41 | File I/O - Reading and Writing to Local Files | 🟡 | A *daily journal* stored as a UTF-8 text file – one entry per line. | [code](src/day_41_file_io/main.py) · [tests](tests/test_day_41.py) · [notes](docs/progress/day-41-reflection.md) |
| 42 | File Directories | 🟡 | A *downloads-folder organiser* – it scaffolds folders, prints a tree, finds files by pattern, sorts files into folders by extension and cleans up, all confined to one sandbox root so a typo can never touch the rest of the disk. | [code](src/day_42_file_directories/main.py) · [tests](tests/test_day_42.py) · [notes](docs/progress/day-42-reflection.md) |
| 43 | Reading and Writing to CSV | 🟡 | A *household expense tracker* that imports a bank CSV export, validates each row, reports bad rows instead of crashing, and exports a category summary. | [code](src/day_43_reading_writing_csv/main.py) · [tests](tests/test_day_43.py) · [notes](docs/progress/day-43-reflection.md) |
| 44 | Introduction to the Pandas Framework | 🟡 | A *coffee-chain sales analysis* – load a CSV into a DataFrame, clean it, add derived columns and answer business questions. | [code](src/day_44_pandas_framework/main.py) · [tests](tests/test_day_44.py) · [notes](docs/progress/day-44-reflection.md) |
| 45 | List Comprehensions | 🟡 | A *web-server log analyser* – raw access-log lines become clean, filtered, transformed lists in one readable expression each. | [code](src/day_45_list_comprehensions/main.py) · [tests](tests/test_day_45.py) · [notes](docs/progress/day-45-reflection.md) |
| 46 | Dictionary Comprehensions | 🟡 | An *online bookshop catalogue* – index products, reprice them, invert lookups and count words in reviews, each with a dict comprehension. | [code](src/day_46_dictionary_comprehensions/main.py) · [tests](tests/test_day_46.py) · [notes](docs/progress/day-46-reflection.md) |
| 47 | Packing and Unpacking Functions in Python | 🟡 | A *GPS route planner* – coordinates, waypoints and connection settings are passed around as tuples and dicts, then unpacked straight into function calls. | [code](src/day_47_packing_unpacking/main.py) · [tests](tests/test_day_47.py) · [notes](docs/progress/day-47-reflection.md) |
| 48 | Creating Desktop GUI Apps with Tkinter | 🟡 | A *restaurant tip splitter* desktop app. The calculation is a pure function (unit-tested everywhere); the GUI is a thin layer of widgets laid out with ``grid`` that reads user input and shows results or errors. | [code](src/day_48_tkinter_gui/main.py) · [tests](tests/test_day_48.py) · [notes](docs/progress/day-48-reflection.md) |
| 49 | Strongly Dynamic Typing | 🟡 | A *product-import pipeline* receiving loosely typed data from spreadsheets and APIs. Python is **dynamic** (names can be rebound to any type at runtime) but **strong** (it refuses to silently mix incompatible types). | [code](src/day_49_strongly_dynamic_typing/main.py) · [tests](tests/test_day_49.py) · [notes](docs/progress/day-49-reflection.md) |
| 50 | Error Handling and Exceptions | 🟡 | A *configuration loader for a microservice* that reads JSON from disk, validates many fields at once, retries flaky reads and logs failures with full context. | [code](src/day_50_error_handling_exceptions/main.py) · [tests](tests/test_day_50.py) · [notes](docs/progress/day-50-reflection.md) |
| 51 | Try / Except / Raise | 🟡 | A *concert ticket booking service* with its own exception hierarchy, so callers can catch errors as broadly or as precisely as they need. | [code](src/day_51_try_except_raise/main.py) · [tests](tests/test_day_51.py) · [notes](docs/progress/day-51-reflection.md) |
| 52 | Working with JSONs | 🟡 | A *weather-station API client* that receives JSON payloads, validates them into typed objects, and serialises its own reports – including types JSON doesn't support natively (datetime, Decimal, dataclasses). | [code](src/day_52_working_with_jsons/main.py) · [tests](tests/test_day_52.py) · [notes](docs/progress/day-52-reflection.md) |
| 53 | Local Persistence | 🟡 | A *language-learning app* that remembers each learner's XP, streak and settings between runs – safely. | [code](src/day_53_local_persistence/main.py) · [tests](tests/test_day_53.py) · [notes](docs/progress/day-53-reflection.md) |
| 54 | Sending Email with Python and SMTP | 🟡 | A *weekly study-report mailer*. It builds a proper MIME message (plain text + HTML + attachment), validates addresses, reads SMTP credentials from the environment and sends with ``smtplib`` over TLS – or does a dry run. | [code](src/day_54_sending_email/main.py) · [tests](tests/test_day_54.py) · [notes](docs/progress/day-54-reflection.md) |
| 55 | Working with Date and Time | 🟡 | A *global team meeting planner* – ages, deadlines, business days and one meeting shown in every teammate's local time. | [code](src/day_55_date_and_time/main.py) · [tests](tests/test_day_55.py) · [notes](docs/progress/day-55-reflection.md) |
| 56 | Hosting Python Code Online with PythonAnywhere | 🟡 | Deploy a tiny *"Quote of the Day" web app* – a standard-library WSGI application that runs locally with ``wsgiref`` and on PythonAnywhere unchanged. | [code](src/day_56_pythonanywhere_hosting/main.py) · [tests](tests/test_day_56.py) · [notes](docs/progress/day-56-reflection.md) |
| 57 | REST APIs & JSON | 🟠 | A *to-do list REST API* simulated in memory. No network: the goal is to understand what HTTP methods mean, which status code each outcome deserves, and how JSON request/response bodies are produced and consumed. | [code](src/day_57_rest_apis_json/main.py) · [tests](tests/test_day_57.py) · [notes](docs/progress/day-57-reflection.md) |
| 58 | HTTP Requests with requests | 🟠 | A *public-holiday dashboard client* that talks to a JSON API (JSONPlaceholder / httpbin for the demo) robustly. | [code](src/day_58_http_requests/main.py) · [tests](tests/test_day_58.py) · [notes](docs/progress/day-58-reflection.md) |
| 59 | Query Parameters, Headers & Payloads | 🟠 | A *job-board search client*. The interesting part is what goes on the wire, so every request is first built offline with ``requests.Request(...).prepare()`` – we can inspect the exact URL, headers and body – and only then sent through a session. | [code](src/day_59_request_parameters_headers_payloads/main.py) · [tests](tests/test_day_59.py) · [notes](docs/progress/day-59-reflection.md) |
| 60 | API Authentication (Client-side) | 🟠 | A *weather-data aggregator* that talks to three providers, each with a different authentication scheme. Secrets come from the environment (optionally a git-ignored ``.env``), are never hard-coded and never printed. | [code](src/day_60_api_authentication/main.py) · [tests](tests/test_day_60.py) · [notes](docs/progress/day-60-reflection.md) |
| 61 | SMS / Notification Automation | 🟠 | A *server-monitoring alerter* that texts the on-call engineer when a health check fails. It integrates with Twilio when credentials and the ``twilio`` package are present, and otherwise falls back to a safe dry run. | [code](src/day_61_sms_notification_automation/main.py) · [tests](tests/test_day_61.py) · [notes](docs/progress/day-61-reflection.md) |
| 62 | Web Scraping with Beautiful Soup | 🟠 | A *quotes research assistant* that collects quotes and authors from quotes.toscrape.com – a site built for scraping practice – *politely*. | [code](src/day_62_web_scraping/main.py) · [tests](tests/test_day_62.py) · [notes](docs/progress/day-62-reflection.md) |
| 63 | Browser Automation with Selenium | 🟠 | A *QA smoke test* for quotes.toscrape.com (a practice site): log in through the form, read quotes from the JavaScript-rendered page that appears only after a delay, and page through results – using Page Objects. | [code](src/day_63_browser_automation_selenium/main.py) · [tests](tests/test_day_63.py) · [notes](docs/progress/day-63-reflection.md) |
| 64 | Iterators & the Iterator Protocol | 🟠 | A *paginated API cursor for a museum collection* – the client hides page requests behind a plain ``for`` loop, exactly like database cursors and cloud SDK paginators do. | [code](src/day_64_iterators_iterator_protocol/main.py) · [tests](tests/test_day_64.py) · [notes](docs/progress/day-64-reflection.md) |
| 65 | Generators & yield | 🟠 | A *smart-meter energy monitor* that streams millions of readings. Generators process them one at a time, so memory stays flat no matter how large the stream is. | [code](src/day_65_generators_yield/main.py) · [tests](tests/test_day_65.py) · [notes](docs/progress/day-65-reflection.md) |
| 66 | Advanced Generators | 🟠 | An *online-shop order pipeline* – raw order lines flow through composable generator stages (parse → validate → enrich → batch), nested category trees are flattened with ``yield from``, and a live revenue tracker receives values via ``send()``. | [code](src/day_66_advanced_generators/main.py) · [tests](tests/test_day_66.py) · [notes](docs/progress/day-66-reflection.md) |
| 67 | Decorators Deep Dive | 🟠 | A *weather-service client toolkit* – cross-cutting concerns (timing, retries, caching per city, rate limiting, input validation) are added to plain functions with decorators instead of being copy-pasted. | [code](src/day_67_decorators_deep_dive/main.py) · [tests](tests/test_day_67.py) · [notes](docs/progress/day-67-reflection.md) |
| 68 | Context Managers | 🟠 | A *laboratory experiment runner*. Instruments must always be switched off, partial results rolled back on failure, and timings recorded – even when an experiment crashes halfway. | [code](src/day_68_context_managers/main.py) · [tests](tests/test_day_68.py) · [notes](docs/progress/day-68-reflection.md) |
| 69 | Descriptors | 🟠 | A *hotel-booking form model* whose fields validate themselves – the same machinery behind Django/SQLAlchemy model fields, ``@property``, ``@classmethod`` and bound methods. | [code](src/day_69_descriptors/main.py) · [tests](tests/test_day_69.py) · [notes](docs/progress/day-69-reflection.md) |
| 70 | Metaclasses (Introduction) | 🟠 | A *document-converter app* with format plugins (Markdown → HTML, CSV → JSON …). Every plugin class must declare its formats and is registered automatically – first with a metaclass, then with the simpler ``__init_subclass__`` hook that is usually the better choice. | [code](src/day_70_metaclasses_intro/main.py) · [tests](tests/test_day_70.py) · [notes](docs/progress/day-70-reflection.md) |
| 71 | Functional Tools | 🟠 | A *music-streaming royalty calculator* – play logs are grouped, accumulated and combined with ``itertools``; pricing rules are pre-configured with ``partial``; expensive look-ups are cached with ``lru_cache``; totals are folded with ``reduce``. | [code](src/day_71_functional_tools/main.py) · [tests](tests/test_day_71.py) · [notes](docs/progress/day-71-reflection.md) |
| 72 | Advanced Typing | 🟠 | A *warehouse-robot fleet manager*. Robots from different vendors share no base class, yet the dispatcher accepts any of them because they satisfy a ``Protocol``. Payloads from the vendors' JSON APIs are described with ``TypedDict``; commands are restricted with ``Literal``; a generic repository works for robots, shelves or anything with an ``id``. | [code](src/day_72_advanced_typing/main.py) · [tests](tests/test_day_72.py) · [notes](docs/progress/day-72-reflection.md) |
| 73 | Concurrency: Threading | 🟠 | A *photo-sharing upload service*. Thumbnails are fetched from slow storage (I/O bound → threads help), view counters are updated from many threads (needs a lock), and uploads flow through a producer/consumer queue. A CPU-bound resize shows why the GIL limits threads for pure-Python work. | [code](src/day_73_concurrency_threading/main.py) · [tests](tests/test_day_73.py) · [notes](docs/progress/day-73-reflection.md) |
| 74 | Concurrency: Multiprocessing | 🟠 | A *satellite-image analysis lab*. Counting "bright pixels" in large tiles is pure CPU work, so it runs in a process pool (each process has its own interpreter and GIL). Tiles are shared through ``shared_memory`` instead of being copied, and a small advisor decides when processes beat threads. | [code](src/day_74_concurrency_multiprocessing/main.py) · [tests](tests/test_day_74.py) · [notes](docs/progress/day-74-reflection.md) |
| 75 | Asyncio Fundamentals | 🟠 | An *airport departures board* that queries several airline status services at once. Each query mostly waits on the network, so one thread with an event loop can overlap all of them. | [code](src/day_75_asyncio_fundamentals/main.py) · [tests](tests/test_day_75.py) · [notes](docs/progress/day-75-reflection.md) |
| 76 | Advanced Asyncio | 🟠 | A *price-comparison engine* that asks many online shops for the price of a product concurrently with ``aiohttp`` – politely (connection limits), safely (timeouts, retries) and streaming results as they arrive. | [code](src/day_76_advanced_asyncio/main.py) · [tests](tests/test_day_76.py) · [notes](docs/progress/day-76-reflection.md) |
| 77 | Logging & Configuration | 🟠 | A *food-delivery dispatch service* that reads its settings from INI, YAML or TOML files (plus environment overrides) and logs to the console for humans and to a rotating JSON file for machines. | [code](src/day_77_logging_configuration/main.py) · [tests](tests/test_day_77.py) · [notes](docs/progress/day-77-reflection.md) |
| 78 | Testing with pytest | 🟠 | A *parcel-shipping quote service* that calls a carrier's rate API. This module is the code under test; ``tests/test_day_78.py`` is the real lesson – it shows fixtures (scopes, factories, teardown, built-ins), parametrisation (ids, stacked parameters), mocking (``Mock(spec=...)``, ``patch``, ``monkeypatch``, call assertions) and coverage. | [code](src/day_78_testing_with_pytest/main.py) · [tests](tests/test_day_78.py) · [notes](docs/progress/day-78-reflection.md) |
| 79 | Packaging & Distribution | 🟠 | Publish *"kitchenconv"*, a tiny cooking-unit converter with a CLI, as a real Python package: generate a ``src``-layout project with a complete ``pyproject.toml``, build a wheel and an sdist offline, inspect what is inside, validate the metadata with ``twine check`` and prepare (not perform) the TestPyPI upload. | [code](src/day_79_packaging_distribution/main.py) · [tests](tests/test_day_79.py) · [notes](docs/progress/day-79-reflection.md) |
| 80 | Profiling & Performance | 🟠 | An *e-commerce nightly report* that got slow as the shop grew. We measure first (``cProfile``, ``timeit``, ``tracemalloc``/``memory_profiler``), find the hotspots, then apply targeted optimisation patterns – and prove the fast version returns exactly the same answer. | [code](src/day_80_profiling_performance/main.py) · [tests](tests/test_day_80.py) · [notes](docs/progress/day-80-reflection.md) |
| 81 | Advanced Regular Expressions | 🟠 | A *customer-support ticket parser* that pulls order numbers, amounts, dates and contact details out of free-text emails, redacts personal data before it reaches the logs, and normalises messy formatting. | [code](src/day_81_advanced_regular_expressions/main.py) · [tests](tests/test_day_81.py) · [notes](docs/progress/day-81-reflection.md) |
| 82 | SQLite & Pure Database Work | 🟠 | A *climbing-gym membership system* – members, passes and check-ins stored in SQLite with a proper schema, constraints, indexes, transactions and versioned migrations, using nothing but the standard library. | [code](src/day_82_sqlite_database/main.py) · [tests](tests/test_day_82.py) · [notes](docs/progress/day-82-reflection.md) |
| 83 | Robust CLI Application | 🔴 | ``habits`` – a *habit-tracker command-line app* with subcommands (``add``, ``done``, ``list``, ``streak``, ``config``), a TOML config file plus environment overrides, logging controlled by ``-v``/``-q``, JSON output for scripting, and proper exit codes. | [code](src/day_83_robust_cli_application/main.py) · [tests](tests/test_day_83.py) · [notes](docs/progress/day-83-reflection.md) |
| 84 | Data Pipeline / ETL Script | 🔴 | A *city air-quality ETL*. Sensor stations drop CSV and JSON-lines files into an inbox folder; the pipeline extracts records lazily, transforms and validates them, quarantines bad rows with reasons, loads clean data into JSON-lines output, and writes a run summary – logging every step. | [code](src/day_84_data_pipeline_etl/main.py) · [tests](tests/test_day_84.py) · [notes](docs/progress/day-84-reflection.md) |
| 85 | Concurrent File / Network Processor | 🔴 | A *podcast-archive mirroring tool*. Episodes are downloaded from a feed server with asyncio (I/O bound, hundreds of sockets on one thread), verified with SHA-256 in a thread pool (disk I/O releases the GIL), and compressed for cold storage in a process pool (pure CPU work). One report tells the operator what succeeded, what failed and why. | [code](src/day_85_concurrent_file_network_processor/main.py) · [tests](tests/test_day_85.py) · [notes](docs/progress/day-85-reflection.md) |
| 86 | Custom Logging & Monitoring Tool | 🔴 | A *payment-gateway monitor*. Every payment attempt is logged as one JSON object (with the request id carried by ``contextvars``), files rotate before they fill the disk, latency and error counts are kept as metrics that render in the Prometheus text format, and an alert handler pages the on-call engineer when errors spike. | [code](src/day_86_custom_logging_monitoring/main.py) · [tests](tests/test_day_86.py) · [notes](docs/progress/day-86-reflection.md) |
| 87 | Plugin-style Architecture | 🔴 | A *team chat-bot* whose commands (``!roll``, ``!weather``, ``!standup`` …) come from plugins. Built-in commands register with a decorator, local plugins are loaded from a folder at runtime, and installed packages contribute commands through ``importlib.metadata`` entry points – a broken or incompatible plugin is reported, never fatal. | [code](src/day_87_plugin_architecture/main.py) · [tests](tests/test_day_87.py) · [notes](docs/progress/day-87-reflection.md) |
| 88 | Automated Report Generator | 🔴 | A *freelance design studio's month-end report*. Time-tracking entries are aggregated per client and project with exact ``Decimal`` money, then rendered three ways: an HTML e-mail body from ``string.Template`` (auto-escaped), a CSV for the accountant, and a one-page PDF written by hand – no third-party PDF library needed. | [code](src/day_88_automated_report_generator/main.py) · [tests](tests/test_day_88.py) · [notes](docs/progress/day-88-reflection.md) |
| 89 | Background Task Runner | 🔴 | A *home-lab backup scheduler*. A small daemon reads job specs such as ``"every 15 minutes"`` or ``"daily at 02:30"``, runs each job as a child process with a timeout, never runs two copies of the same job at once, refuses to start twice (PID file) and shuts down gracefully on SIGTERM. | [code](src/day_89_background_task_runner/main.py) · [tests](tests/test_day_89.py) · [notes](docs/progress/day-89-reflection.md) |
| 90 | Memory-efficient Large File Processor | 🔴 | A *DNA-sequencing lab* receives FASTQ files far larger than RAM. Reads are streamed in fixed-size binary chunks, re-assembled into lines and 4-line records, quality-filtered, counted, and sorted with an *external* merge sort – and ``tracemalloc`` proves the peak memory stays flat while the file grows. | [code](src/day_90_memory_efficient_file_processor/main.py) · [tests](tests/test_day_90.py) · [notes](docs/progress/day-90-reflection.md) |
| 91 | Type-safe Configuration System | 🔴 | An *IoT fleet firmware-rollout service*. Its settings are frozen dataclasses whose **type hints drive parsing**: environment variables such as ``FLEET_DB__PORT=5433`` or ``FLEET_ROLLOUT__REGIONS=eu,us`` are coerced to ``int``, ``bool``, ``Path``, ``Literal``, ``Enum``, tuples and secrets, every problem is reported at once, and secrets never appear in logs. | [code](src/day_91_type_safe_configuration/main.py) · [tests](tests/test_day_91.py) · [notes](docs/progress/day-91-reflection.md) |
| 92 | Test Suite for a Multi-module Package | 🔴 | ``lending`` – a *community library lending system* split into ``models``, ``repository``, ``notifier`` and ``service`` modules. The point of the day is the **test suite**: factory fixtures, a fake repository, mocked notifications, a frozen clock, parametrised business rules and a CI command that enforces >90 % branch coverage for the package. | [code](src/day_92_multi_module_test_suite/main.py) · [tests](tests/test_day_92.py) · [notes](docs/progress/day-92-reflection.md) |
| 93 | Simple Async Network Service | 🔴 | A *pub-quiz game server*. Players connect over TCP with a tiny line protocol (``JOIN``, ``ANSWER``, ``SCORES``, ``QUIT``); questions are broadcast to everyone, only the first correct answer scores, and a hand-written HTTP endpoint serves the live scoreboard as JSON – all on ``asyncio`` streams from the standard library, no framework. | [code](src/day_93_async_network_service/main.py) · [tests](tests/test_day_93.py) · [notes](docs/progress/day-93-reflection.md) |
| 94 | Data Validation & Cleaning Library | 🔴 | ``intake`` – a reusable validation library for a *clinical-trial patient intake* system. Messy form data ("72,5 kg", " F ", "1980/03/07") is cleaned and validated by small composable, type-hinted validators; every error carries its exact path (``visits[1].date``) so a coordinator can fix the whole form in one go. | [code](src/day_94_data_validation_library/main.py) · [tests](tests/test_day_94.py) · [notes](docs/progress/day-94-reflection.md) |
| 95 | Performance-critical Module | 🔴 | A *ride-hailing dispatcher* must find the nearest free driver for every waiting rider, city-wide, several times per second. The same haversine matching is implemented four ways – naive Python, tuned Python with a spatial grid index, vectorised NumPy and (optionally) Numba – then profiled, benchmarked and cross-checked so every fast path returns exactly what the slow, obviously-correct version returns. | [code](src/day_95_performance_critical_module/main.py) · [tests](tests/test_day_95.py) · [notes](docs/progress/day-95-reflection.md) |
| 96 | Packaging a Real Tool | 🔴 | Ship ``tidyfiles`` – a *downloads-folder organiser* that sorts files into ``images/``, ``documents/``, ``archives/`` … – as a release-ready project. Day 79 learned the packaging mechanics; today is the **release engineering** around a working tool: the tool's code is single-sourced into the package, usage docs are generated from the real ``argparse`` parser, the project ships its own tests, versions are bumped with a changelog, a pre-flight check blocks incomplete releases, and a GitHub Actions workflow publishes to TestPyPI with trusted publishing (no API token stored). | [code](src/day_96_packaging_real_tool/main.py) · [tests](tests/test_day_96.py) · [notes](docs/progress/day-96-reflection.md) |
| 97 | Automation Bot Suite | 🔴 | An *apartment-hunting bot*. Every few minutes it scrapes a listings site (politely: ``robots.txt``, paging, a delay), enriches each new flat with commute time from a JSON API, filters by the user's criteria, remembers what it has already reported, and posts matches to a chat webhook with retries – combining the scraping, API, scheduling and notification skills of the course into one pipeline. | [code](src/day_97_automation_bot_suite/main.py) · [tests](tests/test_day_97.py) · [notes](docs/progress/day-97-reflection.md) |
| 98 | Scientific / Simulation Mini-project | 🔴 | An *epidemic outbreak simulator* for a city health department. A deterministic SIR model is integrated in pure Python (RK4) and validated against the analytical final-size equation; NumPy then sweeps hundreds of transmission rates at once, and a stochastic chain-binomial Monte Carlo answers the questions a planner actually asks: *how likely is a major outbreak, and how large could it get?* | [code](src/day_98_scientific_simulation/main.py) · [tests](tests/test_day_98.py) · [notes](docs/progress/day-98-reflection.md) |
| 99 | Observability & Debugging Toolkit | 🔴 | The support team of a *desktop photo-editing app* gets vague bug reports ("it crashed while exporting"). This toolkit turns every crash into a structured, secret-free report (frames, locals, notes, chained causes and exception groups), installs global hooks for the main thread and worker threads, traces nested operations as timed spans, and ships two small custom debuggers: a call tracer (``sys.settrace``) and a watchpoint debugger (``bdb``) that records every change of a variable. | [code](src/day_99_observability_debugging/main.py) · [tests](tests/test_day_99.py) · [notes](docs/progress/day-99-reflection.md) |
| 100 | Portfolio Capstone: Production-ready Python Tool | 🔴 | ``budgetly`` – a *personal expense tracker* you could put on your CV. Five focused modules (models, config, storage, reports, cli) give a command-line tool with layered configuration, SQLite storage with schema migrations, logging, exit codes, CSV export, a ``pyproject.toml`` with a console script, a README, and a test suite holding the package above 90 % branch coverage. | [code](src/day_100_portfolio_capstone/main.py) · [tests](tests/test_day_100.py) · [notes](docs/progress/day-100-reflection.md) |
<!-- course-index:end -->

</details>

The detailed curriculum, with the deliverables for every day, is in [`syllabus.md`](syllabus.md).

---

## Technical Justifications & Explanations

| Decision | Why |
|---|---|
| **One self-contained package per day** | Learners can open any day without reading the others, and a broken day cannot break the rest. |
| **pytest over unittest** | Plain `assert`, fixtures and parametrisation keep tests short enough to read as examples. |
| **ruff + mypy on lesson code** | Learners copy what they see. Lesson code that passes a strict linter and a type checker teaches professional habits by example. |
| **A `DELIVERABLES` map in every module** | Each syllabus promise points to real code, and CI checks that the target exists. |
| **Generated reflections and README tables** | Writing facts by hand invites drift. Generating them from code and notes, then verifying them in CI, keeps the course truthful. |
| **No network in tests** | Tests must pass offline, on every OS and every time. Network code is tested against local servers on `127.0.0.1`. |
| **`sqlite3` without an ORM (Days 82, 100)** | Writing parameterised SQL by hand shows what an ORM does for you, and why string-formatted SQL is dangerous. |
| **`requests` for synchronous HTTP and `aiohttp` for async** | `requests` is the most widely used client to learn first. `aiohttp` provides both an async client and a test server in one dependency. |
| **`schedule` rather than APScheduler (Days 89, 97)** | Its readable API (`every(15).minutes`) keeps attention on process management, not on configuring a scheduler. |
| **`Decimal` for money** | Binary floats cannot represent cents exactly. Every financial example rounds deliberately with `Decimal`. |
| **hatchling for packaging examples** | A modern, standards-based build backend with minimal configuration. Day 79 compares it with setuptools and Poetry. |
| **CI on three Python versions and three operating systems** | Learners use Windows, macOS and Linux. Path, signal and MIME-type differences are caught in CI, not on a learner's machine. |

---

## Project Timeline & Deadlines

| Milestone | Target | Status |
|---|---|---|
| Phases 1–3 · Days 1–63 (fundamentals, intermediate, APIs) | Mar–Sep 2026 | ✅ Done |
| Phases 4–5 · Days 64–100 (advanced, capstones) | Oct 2026 | ✅ Done |
| Community files, licences, README and syllabus restructure | Oct 2026 | ✅ Done |
| `v1.0.0` release tag and protected default branch | Oct 2026 | ⏳ Next |
| Exercises with failing-first tests, Days 1–3 (pilot) | Nov 2026 | ⬜ Planned |
| Documentation site and Codespaces setup | Dec 2026 | ⬜ Planned |
| Exercises for Days 1–56 and a learner helper CLI | Q1 2027 | ⬜ Planned |
| Quizzes, spaced-repetition flashbacks, first learner cohort | Q1–Q2 2027 | ⬜ Planned |
| Exercises for all 100 days · `v2.0.0` | Q3 2027 | ⬜ Planned |

The full twelve-month plan, covering the contributor programme, learner experience,
sponsorship and governance, is in [`learning_develop.md`](learning_develop.md).

---

## Contact & Author Information

**Bhargavi Badal**, author and maintainer

<p>
  <a href="https://github.com/OdeToTheWind"><img src="https://img.shields.io/badge/GitHub-OdeToTheWind-181717?style=flat-square&logo=github" alt="GitHub: OdeToTheWind"></a>
  <a href="https://github.com/OdeToTheWind/pro-python-mastery/issues/new/choose"><img src="https://img.shields.io/badge/Report-an%20issue-3776ab?style=flat-square" alt="Report an issue"></a>
</p>

* **Found a mistake or have an idea?** [Open an issue](https://github.com/OdeToTheWind/pro-python-mastery/issues/new/choose). Templates are provided for content errors, bugs and ideas.
* **Want to contribute?** Read [CONTRIBUTING.md](CONTRIBUTING.md) and the [Code of Conduct](CODE_OF_CONDUCT.md).
* **Found a security issue?** Report it privately, as described in [SECURITY.md](SECURITY.md).
* **Using the course in teaching?** Please cite it using [CITATION.cff](CITATION.cff).

### Licence

The **code** (`src/`, `tests/`, `scripts/`) is released under the [MIT License](LICENSE). The
**course text and images** (`README.md`, `syllabus.md`, `docs/` and the other Markdown files)
are released under [CC BY 4.0](LICENSE-CONTENT). You may reuse and adapt both, including in
paid courses, as long as you credit **"Pro Python Mastery" by Bhargavi Badal**.
