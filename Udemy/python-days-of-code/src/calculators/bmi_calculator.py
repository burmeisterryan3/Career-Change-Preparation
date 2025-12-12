"""Calculate BMI."""

from pydantic import PositiveFloat, PositiveInt, validate_call


@validate_call
def bmi_calculator(
    height: PositiveFloat, weight: PositiveInt
) -> PositiveFloat:
    """Compute BMI - weight(kg) / height^2 (m^2).

    Args:
        height: meters
        weight: kilograms

    Returns:
        BMI
    """
    return round(weight / height**2, 1)


@validate_call
def bmi_characterization(bmi: float) -> str:
    """Categorically characterizes BMI."""
    if bmi < 18.5:
        return "underweight"
    elif bmi < 25:
        return "normal weight"
    elif bmi < 30:
        return "slightly overweight"
    elif bmi < 35:
        return "obese"
    else:
        return "clinically obese"


print("Welcome to the BMI calculator!")
height = float(input("What is your height in meters?  "))
weight = int(input("How much do you weight in kilograms?  "))
bmi = bmi_calculator(height, weight)
print(f"Your have a BMI of: {bmi} - {bmi_characterization(bmi)}.")
