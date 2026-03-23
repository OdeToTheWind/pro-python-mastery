# src/day_07_converting_types/main.py
"""
Day 7: Type Conversion (Casting) – Interactive Explorer v2
User declares what type they intend → pre-conversion → final target conversion
"""

def get_raw_input() -> str | None:
    raw = input("Your value → ").strip()
    if raw.lower() in ('quit', 'q', 'exit'):
        return None
    return raw


def show_initial_info(raw: str):
    print(f"\n┌─ You entered (raw string): {raw!r}")
    print(f"│  Received type: str (everything from input() is str)")
    print("└" + "─" * 60)


def get_intended_type() -> str:
    options = {
        "1": "int", "2": "float", "3": "str", "4": "bool",
        "5": "list / tuple / set / dict", "6": "other / unknown"
    }
    print("\nWhat type do you think this value represents?")
    for k, v in options.items():
        print(f"  {k}) {v}")
    while True:
        choice = input("→ ").strip()
        if choice in options:
            return options[choice]
        print("Pick 1–6.")


def pre_convert_to_intended(raw: str, intended: str) -> tuple[any, str | None]:
    """Try to interpret the string as the intended type"""
    if intended == "str":
        return raw, None

    try:
        if intended == "int":
            return int(raw), None
        if intended == "float":
            return float(raw), None
        if intended == "bool":
            if raw.lower() in ('true', '1', 'yes', 'on'):
                return True, None
            if raw.lower() in ('false', '0', 'no', 'off', ''):
                return False, None
            return raw, "bool only accepts true/false/1/0/yes/no/on/off/empty"
        if intended in ("list / tuple / set / dict", "other / unknown"):
            return raw, "Keeping as string — complex types need special syntax"
    except ValueError as e:
        return raw, f"Cannot interpret as {intended}: {e}"

    return raw, "No pre-conversion attempted"


def get_target_type() -> str:
    options = {
        "1": "int", "2": "float", "3": "str", "4": "bool",
        "5": "list", "6": "tuple", "7": "set", "8": "dict"
    }
    print("\nChoose FINAL target type:")
    for k, v in options.items():
        print(f"  {k}) {v}")
    while True:
        choice = input("→ ").strip()
        if choice in options:
            return options[choice]
        print("Pick 1–8.")


def attempt_final_conversion(value: any, target: str) -> tuple[any, str | None]:
    try:
        if target == "int":    return int(value), None
        if target == "float":  return float(value), None
        if target == "str":    return str(value), None
        if target == "bool":   return bool(value), None
        if target == "list":   return list(value), None
        if target == "tuple":  return tuple(value), None
        if target == "set":    return set(value), None
        if target == "dict":   return dict(value), None
    except (ValueError, TypeError) as e:
        return None, str(e)
    return None, "Unsupported target"


def show_result(raw: str, intended: str, pre_value: any, pre_err: str | None,
                target: str, final_value: any, final_err: str | None):
    print("\n" + "═" * 70)
    print(f"Input (raw) : {raw!r}")
    print(f"Intended as : {intended}")
    if pre_err:
        print(f"Pre-conversion failed: {pre_err}")
        print(f"  → kept as: {pre_value!r} ({type(pre_value).__name__})")
    else:
        print(f"Pre-converted to: {pre_value!r} ({type(pre_value).__name__})")

    print(f"Target type : {target}")
    if final_err:
        print(f"✗ Final conversion failed: {final_err}")
    else:
        print(f"✓ Succeeded → {final_value!r} ({type(final_value).__name__})")
    print("═" * 70)


def main():
    print("Day 7 – Type Conversion Explorer (Improved)")
    print("Everything starts as str. You declare intended type → then choose target.\n")

    while True:
        print("\n" + "─" * 60)
        print("Enter a value (plain text or number, 'quit' to exit)")
        print("─" * 60)

        raw = get_raw_input()
        if raw is None:
            break

        show_initial_info(raw)

        intended = get_intended_type()

        pre_value, pre_err = pre_convert_to_intended(raw, intended)

        target = get_target_type()

        final_value, final_err = attempt_final_conversion(pre_value, target)

        show_result(raw, intended, pre_value, pre_err, target, final_value, final_err)

    print("\nSession ended. You now better understand str → other types → final type.\n")


if __name__ == "__main__":
    main()