# src/day_06_data_types/main.py
"""
Day 6: Python Built-in Data Types – Interactive Explorer
Discover types, mutability, conversions, and basic behaviors with your own inputs.
"""

import ast  # for safe literal evaluation (advanced input)


def get_user_value(prompt: str) -> tuple[any, str]:
    """Get input and try to evaluate it as literal (int, float, list, etc.) or keep as str"""
    raw = input(prompt).strip()
    if raw.lower() in ('quit', 'q', 'exit'):
        return None, raw

    try:
        # Safely evaluate simple literals: 42, 3.14, True, [1,2,3], {"a":1}, etc.
        value = ast.literal_eval(raw)
    except (ValueError, SyntaxError):
        # Fallback to string if not a literal
        value = raw

    return value, raw


def show_type_info(value: any, original_input: str):
    """Display detailed info about the value"""
    t = type(value).__name__
    print(f"\n┌── You entered: {original_input!r}")
    print(f"│   Interpreted as: {value!r}")
    print(f"│   Type:          {t} ({type(value)})")
    print(f"│   ID:            {id(value):x}")
    print(f"│   Mutable?       {'Yes' if hasattr(value, '__setitem__') or isinstance(value, (set, dict)) else 'No'}")
    print(f"│   Hashable?      {'Yes' if isinstance(value, (int, float, bool, str, tuple, frozenset)) else 'No (unhashable)'}")

    # Length / count for sequences & collections
    if hasattr(value, '__len__'):
        print(f"│   Length:        {len(value)}")

    # Some type-specific extras
    if isinstance(value, (int, float)):
        print(f"│   As int:        {int(value) if isinstance(value, float) else value}")
        print(f"│   As float:      {float(value)}")
    elif isinstance(value, bool):
        print(f"│   Truthy?        {bool(value)}")
    elif isinstance(value, str):
        print(f"│   Upper:         {value.upper()}")
        print(f"│   Length:        {len(value)} chars")
        print(f"│   As list:       {list(value)}")
    elif isinstance(value, (list, tuple)):
        print(f"│   First item:    {value[0] if value else 'empty'}")
    elif isinstance(value, dict):
        print(f"│   Keys:          {list(value.keys())}")
    elif isinstance(value, set):
        print(f"│   Elements:      {sorted(value) if all(isinstance(x, (int,str)) for x in value) else 'mixed types'}")
    elif value is None:
        print("│   → The famous None (absence of value)")

    print("└" + "─" * 60)


def explain_data_types_overview():
    print("\n" + "═" * 70)
    print("Python Built-in Data Types Overview (Python 3.14 era)")
    print("═" * 70)
    print("Category       | Types                          | Mutable? | Ordered? | Hashable?")
    print("───────────────┼────────────────────────────────┼──────────┼──────────┼───────────")
    print("Numeric        | int, float, bool, complex      | No       | —        | Yes       ")
    print("Text/Sequence  | str                            | No       | Yes      | Yes       ")
    print("Sequences      | list, tuple, range             | list:Yes | Yes      | tuple+range:Yes ")
    print("Mappings       | dict                           | Yes      | Yes (3.7+) | No      ")
    print("Sets           | set, frozenset                 | set:Yes  | No       | frozenset:Yes ")
    print("Binary         | bytes, bytearray, memoryview   | bytearray:Yes | Yes | bytes+memoryview:Yes ")
    print("None           | NoneType                       | No       | —        | Yes       ")
    print("═" * 70)
    print("• Mutable = can change after creation (list.append(), dict['key']=val)")
    print("• Hashable = can be used as dict key or set element")
    print("• Use type(value), isinstance(value, list), etc. to check types")
    print("═" * 70)


def main():
    print("Welcome to Day 6 – Python Built-in Data Types Explorer!")
    print("Enter almost any Python literal or text — see what type it becomes!\n")

    explain_data_types_overview()

    print("\nExamples you can try:")
    print("  42               → int")
    print("  3.14             → float")
    print("  True             → bool")
    print("  'hello'          → str")
    print("  [1, 2, 'a']      → list")
    print("  (10, 20)         → tuple")
    print("  {'name': 'Alex', 'age': 30}  → dict")
    print("  {1, 2, 3}        → set")
    print("  None             → NoneType")
    print("  anything else    → treated as str\n")

    while True:
        print("\n" + "─" * 60)
        print("Enter a value (or 'quit' to exit)")
        print("─" * 60)

        value, original = get_user_value("Your input → ")
        if value is None:
            break

        show_type_info(value, original)

    print("\nGreat exploration! You now understand Python's core data types.")
    print("Remember: type() tells you what it is, isinstance() checks safely.\n")


if __name__ == "__main__":
    main()