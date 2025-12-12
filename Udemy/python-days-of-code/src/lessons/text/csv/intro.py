import csv

import pandas as pd


def with_readlines():
    """Read using the text IO wrapper."""
    with open("weather_data.csv") as f:
        rows = [line.strip().split(",") for line in f.readlines()]
        print(rows)


def with_csv_reader():
    """Reading using python's csv library."""
    with open("weather_data.csv") as f:
        rows = csv.reader(f)
        days, temps, conditions = zip(*rows)
        print(f"days: {days[1:]}")
        print(f"temperatures: {temps[1:]}")
        print(f"statuses: {conditions[1:]}")


def with_pandas():
    """Read using python's pandas library."""
    return pd.read_csv("weather_data.csv")


def average(df: pd.DataFrame, col: str):
    """Compute the average within a given column."""
    print(df[col].mean())


def maximum(df: pd.DataFrame, col: str):
    """Compute the maximum within a given column."""
    print(df[col].max())


def convert_to_Fahrenheit(deg: float):
    """Convert the degrees in Celsius to Fahrenheit."""
    return deg * (9 / 5) + 32


if __name__ == "__main__":
    # with_readlines()
    # with_csv_reader()
    df = with_pandas()
    average(df, "temp")
    maximum(df, "temp")

    print(df[df["temp"] == df["temp"].max()]["day"].values[0])
    print(convert_to_Fahrenheit(df[df["day"] == "Monday"]["temp"][0]))
