"""Day 2."""

from pydantic import PositiveFloat, PositiveInt, validate_call


@validate_call
def tip_calculator(
    bill: PositiveFloat, percent: PositiveInt, splits: PositiveInt = 1
) -> PositiveFloat:
    """Return the per person cost for a bill and a given tip percentage."""
    # Without pydantic type checking
    # if bill < 0 or percent < 0 or splits < 0:
    #     raise ValueError("Bill, percent, and splits cannot be negative")

    return round(bill / splits * (1 + percent / 100), 2)


print("Welcome to the tip calculator!")
bill = float(input("What was the total bill?  $"))
percent = int(
    input("How much tip would you like to give? 10, 15, 20, or 25?  ")
)
splits = int(input("How many people to split the bill?  "))
print(f"Each person should pay ${tip_calculator(bill, percent, splits):.2f}.")
