import pandas as pd

FILENAME = "2018_Central_Park_Squirrel_Census_-_Squirrel_Data.csv"


def read_file():
    """Read the squirrel census data."""
    return pd.read_csv(FILENAME)


if __name__ == "__main__":
    df = read_file()
    df["Primary Fur Color"].value_counts().reset_index().to_csv(
        "squirrel_fur_counts.csv"
    )
