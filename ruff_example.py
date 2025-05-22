"""Example file demonstrating Ruff formatting and linting.

This file shows how Ruff will format and lint Python code.
It includes examples of common issues that Ruff will catch and fix.
"""
from typing import Any


def messy_function(a: int, b: int = 5, c: int | None = None) -> int | None:
    """Example function with formatting issues.

    Args:
        a: First parameter
        b: Second parameter with default
        c: Optional parameter

    Returns:
        The result of a calculation
    """
    if a is None:  # fixed comparison to None
        return None

    # Split long line into more readable parts
    really_long_result = (
        a + b + c
        if c is not None
        else a + b + sum([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
    )

    return really_long_result


class BadlyFormattedClass:
    """Class with bad indentation."""

    def __init__(self) -> None:
        """Initialize the class with x and y coordinates."""
        self.x = 10
        self.y = 20

    def badly_spaced_method(self, input_param: int) -> int:
        """Method with bad spacing.

        Args:
            input_param: The input parameter to add

        Returns:
            The sum of x, y and input_param
        """
        return self.x + self.y + input_param


def missing_type_hints(input_data: dict[str, Any]) -> str:
    """Function missing type hints.

    Args:
        input_data: Dictionary containing the input data

    Returns:
        The value for 'key' or 'default' if key doesn't exist
    """
    return input_data.get("key", "default")


if __name__ == "__main__":
    print(messy_function(10))
    obj = BadlyFormattedClass()
    print(obj.badly_spaced_method(30))
    print(missing_type_hints({"key": "value"}))
