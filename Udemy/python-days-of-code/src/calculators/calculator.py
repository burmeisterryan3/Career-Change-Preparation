"""Day 10."""

from collections.abc import Callable

LOGO = r"""
 _____________________
|  _________________  |
| | Pythonista   0. | |  .----------------.  .----------------.  .----------------.  .----------------. 
| |_________________| | | .--------------. || .--------------. || .--------------. || .--------------. |
|  ___ ___ ___   ___  | | |     ______   | || |      __      | || |   _____      | || |     ______   | |
| | 7 | 8 | 9 | | + | | | |   .' ___  |  | || |     /  \     | || |  |_   _|     | || |   .' ___  |  | |
| |___|___|___| |___| | | |  / .'   \_|  | || |    / /\ \    | || |    | |       | || |  / .'   \_|  | |
| | 4 | 5 | 6 | | - | | | |  | |         | || |   / ____ \   | || |    | |   _   | || |  | |         | |
| |___|___|___| |___| | | |  \ `.___.'\  | || | _/ /    \ \_ | || |   _| |__/ |  | || |  \ `.___.'\  | |
| | 1 | 2 | 3 | | x | | | |   `._____.'  | || ||____|  |____|| || |  |________|  | || |   `._____.'  | |
| |___|___|___| |___| | | |              | || |              | || |              | || |              | |
| | . | 0 | = | | / | | | '--------------' || '--------------' || '--------------' || '--------------' |
| |___|___|___| |___| |  '----------------'  '----------------'  '----------------'  '----------------' 
|_____________________|
"""


def operations(operator: str) -> Callable[[float, float], float]:
    """Return the operator based on the user input."""
    return OPERATIONS[operator]


def add(n1: float, n2: float) -> float:
    """Add two numbers."""
    return n1 + n2


def subtract(n1: float, n2: float) -> float:
    """Subtract two numbers."""
    return n1 - n2


def multiply(n1: float, n2: float) -> float:
    """Multiply two numbers."""
    return n1 * n2


def divide(dividend: float, divisor: float) -> float:
    """Divide two numbers."""
    return dividend / divisor


OPERATIONS = {"+": add, "-": subtract, "*": multiply, "/": divide}


def get_num_input(first=False) -> float:
    """Get the user's number input."""
    if first:
        adj = "first"
    else:
        adj = "next"

    while True:
        try:
            return float(input(f"What's the {adj} number? "))
        except ValueError:
            continue


def get_operation() -> str:
    """Get operation from user."""
    operation = ""
    while operation not in OPERATIONS:
        operation = input("Pick an operation. ")

    return operation


if __name__ == "__main__":
    print(f"{LOGO}\n\n")
    new_computation = True
    while new_computation:
        num1 = get_num_input(first=True)
        print("\n".join(OPERATIONS))

        should_continue = True
        while should_continue:
            operation = get_operation()
            num2 = get_num_input()

            result = operations(operation)(num1, num2)
            print(f"{num1} {operation} {num2} = {result}")

            user_input = input(
                f"Type 'c' to continue calculating with {result}, 'n' to start a new calculation, or 'q' to quit. "
            )

            if user_input == "c":
                num1 = result
            else:
                should_continue = False
                if user_input == "q":
                    new_computation = False
