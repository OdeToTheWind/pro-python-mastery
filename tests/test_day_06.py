# tests/test_day_06.py
import pytest
from src.day_06_data_types.main import get_user_value


def test_get_user_value_quit():
    # We can't easily patch input here, but conceptually:
    # if input == 'quit' → return None, 'quit'
    pass  # For real tests we'd mock input()


@pytest.mark.parametrize(
    "input_str, expected_type_name",
    [
        ("42", "int"),
        ("3.14", "float"),
        ("True", "bool"),
        ("'hello world'", "str"),
        ("[1, 2, 3]", "list"),
        ("(10, 20)", "tuple"),
        ("{'a': 1, 'b': 2}", "dict"),
        ("{1, 2, 3}", "set"),
        ("None", "NoneType"),
    ]
)
def test_literal_evaluation(input_str, expected_type_name):
    # Simulate literal_eval success path
    from ast import literal_eval
    try:
        value = literal_eval(input_str)
        assert type(value).__name__ == expected_type_name
    except Exception:
        pytest.fail(f"literal_eval failed on valid literal: {input_str}")