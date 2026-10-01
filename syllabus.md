# Python Project Syllabus

> **How status is verified.** A day is marked **Covered** only when it has
> `src/day_XX_<topic>/main.py` with a `DELIVERABLES` map, `tests/test_day_XX.py`
> that imports and exercises that code, and `docs/progress/day-XX-reflection.md`
> that lists the same deliverables. `tests/test_syllabus_sync.py` enforces this
> in CI, so the table below cannot drift from the code.

| Day | Topic | Key Learnings/Deliverables | Topic Level | Status of covered |
|-----|-------|---------------------------|-------------|------------------|
| 01 | Variables, Type Hinting & Scoping | Strict typing with PEP 484/695, f-strings, scope rules, local vs global vs nonlocal | Beginner | Covered |
| 02 | String Manipulation | Advanced string methods, cleaning input, string formatting and alignment | Beginner | Covered |
| 03 | Input & Print Functions | User input validation, type conversion, interactive console applications | Beginner | Covered |
| 04 | Variable Naming Rules | PEP 8 naming conventions, reserved keywords, descriptive names and constants | Beginner | Covered |
| 05 | Mathematical Operations | Arithmetic operators, precedence, floor division, safe division handling | Beginner | Covered |
| 06 | Built-in Data Types | int, float, bool, str, list, tuple, dict, set, mutability and type checks | Beginner | Covered |
| 07 | Converting Types (Casting) | int(), float(), str(), bool(), list(), tuple(), set(), dict(), ValueError vs TypeError | Beginner | Covered |
| 08 | If / Elif / Else Conditionals | Comparison operators, nested logic, truthy/falsy values, chained conditionals | Beginner | Covered |
| 09 | Logical Operations | and, or, not, short-circuit evaluation, combining comparisons and access control | Beginner | Covered |
| 10 | Randomisation | random module, randint(), choice(), shuffle(), password generation, games | Beginner | Covered |
| 11 | Error Handling | try/except/else/finally, common exceptions and robust user input handling | Beginner | Covered |
| 12 | Functions | Parameters, default arguments, *args, **kwargs, docstrings, type hints | Beginner | Covered |
| 13 | For Loops | for loops, range(), enumerate(), zip(), nested loops, tables and iteration | Beginner | Covered |
| 14 | Code Blocks and Indentation | Python indentation rules, loop and function blocks, common IndentationError fixes | Beginner | Covered |
| 15 | While Loops | while loops, break, continue, while-else, input validation and games | Beginner | Covered |
| 16 | Flowchart Programming | Translating logic flowcharts into if-elif-else and loop structures | Beginner | Covered |
| 17 | Positional and Keyword Arguments | Positional vs keyword arguments, defaults and argument flexibility | Beginner | Covered |
| 18 | Python Dictionaries and Lists | List and dict methods, inventory management, shopping cart logic | Beginner | Covered |
| 19 | Nested Collections | List of dicts, dict of lists, nested structures and classroom systems | Beginner | Covered |
| 20 | Returning Functions | return statements, returning multiple values, early returns and function composition | Beginner | Covered |
| 21 | Return vs. Print | Differentiating output vs return values, reusability and function design | Beginner | Covered |
| 22 | Docstrings vs. Comments | # comments vs """ docstrings, documentation standards and metadata | Beginner | Covered |
| 23 | Scope and Local/Global Variables | LEGB rule, global and nonlocal usage, and good scoping practices | Beginner | Covered |
| 24 | Debugging Techniques | Print debugging, tracebacks, breakpoints, and systematic bug fixing | Beginner | Covered |
| 25 | Local Development Environment Setup | Virtual environments, project structure, and local development best practices | Intermediate | Covered |
| 26 | PyCharm Tips and Tricks | IDE productivity, debugging, refactoring tools, templates and shortcuts | Intermediate | Covered |
| 27 | Python Object Oriented Programming | OOP fundamentals, classes, objects, encapsulation and abstraction | Intermediate | Covered |
| 28 | Creating Classes in Python | Defining classes, __init__, instance attributes and methods | Intermediate | Covered |
| 29 | Using External Python Modules / Import | import statements, package installation, and module organization | Intermediate | Covered |
| 30 | Getting / Setting Attributes | @property, getters, setters, and controlled attribute access | Intermediate | Covered |
| 31 | Python Methods | Instance methods, class methods and static methods | Intermediate | Covered |
| 32 | Class Initialisers | __init__ constructors, defaults, validation and object setup | Intermediate | Covered |
| 33 | Module Aliasing | import module as alias, code organization and readability | Intermediate | Covered |
| 34 | Optional, Required and Default Parameters | Advanced parameter handling, *args, **kwargs and ordering rules | Intermediate | Covered |
| 35 | Event Listeners | Event-driven patterns and callback-based interactions | Intermediate | Covered |
| 36 | Python Instances and State | Instance variables, state tracking and object lifecycle patterns | Intermediate | Covered |
| 37 | Python Turtle | Graphics, shapes, drawing logic and animations using Turtle | Intermediate | Covered |
| 38 | Game Development with Python and OOP | Simple game-building using classes, state and user interaction | Intermediate | Covered |
| 39 | Python Inheritance | Single and multiple inheritance, super(), and method overriding | Intermediate | Covered |
| 40 | Python Slice Function | Advanced slicing techniques for lists and strings | Intermediate | Covered |
| 41 | File I/O - Reading and Writing to Local Files | open(), with statements, and file handling patterns | Intermediate | Covered |
| 42 | File Directories | os and pathlib, folder navigation and file system work | Intermediate | Covered |
| 43 | Reading and Writing to CSV | CSV processing, tabular data import/export and parsing | Intermediate | Covered |
| 44 | Introduction to the Pandas Framework | DataFrames, data analysis basics with pandas | Intermediate | Covered |
| 45 | List Comprehensions | Concise creation, filtering and transformation of sequences | Intermediate | Covered |
| 46 | Dictionary Comprehensions | Efficient dictionary creation and transformation | Intermediate | Covered |
| 47 | Packing and Unpacking Functions in Python | Advanced argument unpacking with * and ** | Intermediate | Covered |
| 48 | Creating Desktop GUI Apps with Tkinter | GUI building with widgets, layouts and user input | Intermediate | Covered |
| 49 | Strongly Dynamic Typing | Python's dynamic typing behaviour and practical implications | Intermediate | Covered |
| 50 | Error Handling and Exceptions | Advanced exception handling techniques and best practices | Intermediate | Covered |
| 51 | Try / Except / Raise | Raising custom exceptions and exception hierarchy design | Intermediate | Covered |
| 52 | Working with JSONs | JSON serialization, parsing and payload handling | Intermediate | Covered |
| 53 | Local Persistence | Saving and loading application state between runs | Intermediate | Covered |
| 54 | Sending Email with Python and SMTP | Automating email delivery with smtplib | Intermediate | Covered |
| 55 | Working with Date and Time | datetime usage, calculations, formatting and timezone awareness | Intermediate | Covered |
| 56 | Hosting Python Code Online with PythonAnywhere | Cloud deployment basics and live app hosting | Intermediate | Covered |
| 57 | REST APIs & JSON | HTTP methods, status codes, serialization and API payload processing | Advanced | Covered |
| 58 | HTTP Requests with requests | GET/POST requests, response handling, sessions and timeouts | Advanced | Covered |
| 59 | Query Parameters, Headers & Payloads | Query strings, custom headers, forms and JSON request bodies | Advanced | Covered |
| 60 | API Authentication (Client-side) | API keys, Bearer tokens, Basic Auth and environment variables | Advanced | Covered |
| 61 | SMS / Notification Automation | Twilio integration and secure secrets management | Advanced | Covered |
| 62 | Web Scraping with Beautiful Soup | HTML parsing, selectors and ethical data extraction | Advanced | Covered |
| 63 | Browser Automation with Selenium | Locator strategies, waits, form filling and dynamic page interactions | Advanced | Covered |
| 64 | Iterators & the Iterator Protocol | __iter__, __next__, and custom iterators | Advanced | Covered |
| 65 | Generators & yield | Generator functions, lazy evaluation, and memory benefits | Advanced | Covered |
| 66 | Advanced Generators | yield from, generator pipelines, and sending values | Advanced | Covered |
| 67 | Decorators Deep Dive | Function decorators, @wraps, parameterized decorators, and class-based decorators | Advanced | Covered |
| 68 | Context Managers | The with statement, __enter__, __exit__, and contextlib | Advanced | Covered |
| 69 | Descriptors | Data and non-data descriptors; how @property works under the hood | Advanced | Covered |
| 70 | Metaclasses (Introduction) | type, custom metaclasses, and when or when not to use them | Advanced | Covered |
| 71 | Functional Tools | itertools, functools, partial, lru_cache, and reduce | Advanced | Planned |
| 72 | Advanced Typing | Protocol, TypeVar, Generic, TypedDict, Literal, and checking with mypy/pyright | Advanced | Planned |
| 73 | Concurrency: Threading | threading, locks, queues, and GIL implications | Advanced | Planned |
| 74 | Concurrency: Multiprocessing | Process pools, shared memory, and choosing processes vs. threads | Advanced | Planned |
| 75 | Asyncio Fundamentals | Event loop, coroutines, async/await, gather, and create_task | Advanced | Planned |
| 76 | Advanced Asyncio | Async context managers, async iterators, and concurrent HTTP with aiohttp | Advanced | Planned |
| 77 | Logging & Configuration | Logging handlers, formatters, levels, configparser, YAML, and TOML | Advanced | Planned |
| 78 | Testing with pytest | Fixtures, parametrization, mocking, and coverage | Advanced | Planned |
| 79 | Packaging & Distribution | pyproject.toml, setuptools/hatch/poetry, wheels, and test publishing to PyPI | Advanced | Planned |
| 80 | Profiling & Performance | cProfile, timeit, memory_profiler, and optimization patterns | Advanced | Planned |
| 81 | Advanced Regular Expressions | Complex patterns, groups, lookarounds, and the re module | Advanced | Planned |
| 82 | SQLite & Pure Database Work | sqlite3, transactions, context managers, and basic schema design without an ORM | Advanced | Planned |
| 83 | Robust CLI Application | argparse or click/typer, subcommands, configuration, and logging | Capstone | Planned |
| 84 | Data Pipeline / ETL Script | Generators, pathlib, CSV/JSON, error handling, and logging | Capstone | Planned |
| 85 | Concurrent File / Network Processor | Thread/process pools or asyncio for I/O-bound work | Capstone | Planned |
| 86 | Custom Logging & Monitoring Tool | Structured logging, log rotation, and basic metrics | Capstone | Planned |
| 87 | Plugin-style Architecture | Entry points, dynamic loading, and decorator-based registration | Capstone | Planned |
| 88 | Automated Report Generator | Data aggregation, string.Template or Jinja2, and PDF/CSV output | Capstone | Planned |
| 89 | Background Task Runner | Scheduling with schedule or APScheduler and process management | Capstone | Planned |
| 90 | Memory-efficient Large File Processor | Generators, streaming, and chunking | Capstone | Planned |
| 91 | Type-safe Configuration System | Pydantic or dataclasses, validation, and environment variables | Capstone | Planned |
| 92 | Test Suite for a Multi-module Package | High coverage, fixtures, mocks, and CI-friendly structure | Capstone | Planned |
| 93 | Simple Async Network Service | An asyncio TCP/HTTP server with the standard library or aiohttp, without a full framework | Capstone | Planned |
| 94 | Data Validation & Cleaning Library | Reusable validators, custom exceptions, and type hints | Capstone | Planned |
| 95 | Performance-critical Module | Profiling, optimization, and optional Cython/Numba | Capstone | Planned |
| 96 | Packaging a Real Tool | Complete pyproject.toml, CLI entry point, documentation, tests, and TestPyPI publishing | Capstone | Planned |
| 97 | Automation Bot Suite | Combining scraping, APIs, scheduling, and notifications | Capstone | Planned |
| 98 | Scientific / Simulation Mini-project | NumPy and a pure-Python simulation or Monte Carlo project | Capstone | Planned |
| 99 | Observability & Debugging Toolkit | Advanced traceback handling, custom debuggers, and structured logs | Capstone | Planned |
| 100 | Portfolio Capstone: Production-ready Python Tool | A useful multi-module tool with CLI, tests (>90% coverage), logging, config, packaging, and docs | Capstone | Planned |

- **Phase 1: Beginner Fundamentals (Days 1–24) — Completed! 🎓**
- **Phase 2: Intermediate Python (Days 25–56) — Completed! 🎓**
- **Phase 3: API Clients, Automation & Data Acquisition (Days 57–63) — Completed! 🎓**
- **Phase 4: Advanced Python Language & Tooling (Days 64–82) — In progress (Days 64–70 covered)**
- **Phase 5: Capstone-Style Pure-Python Projects (Days 83–100) — Planned**

