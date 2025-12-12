"""Day 5."""

from pydantic import validate_call


@validate_call
def fizzbuzz() -> str:
    """Plays the fizz buzz game to 100.

    When divisible by 3, the output should be "Fizz"
    When divisible by 5, the output should be "Buzz"
    When divisible by 5 and 3, i.e., 15, the output should be "FizzBuzz"

    Returns:
        A string with each of the fizzbuzz evaluations on a separate line
    """
    fizzbuzz = ""
    for num in range(1, 101):
        if num % 15 == 0:
            fizzbuzz += "FizzBuzz\n"
        elif num % 5 == 0:
            fizzbuzz += "Buzz\n"
        elif num % 3 == 0:
            fizzbuzz += "Fizz\n"
        else:
            fizzbuzz += str(num) + "\n"

    return fizzbuzz  # remove the final "\n" character


print(fizzbuzz())
