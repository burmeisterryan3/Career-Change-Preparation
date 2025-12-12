# TODO: Create a letter using starting_letter.txt
# for each name in invited_names.txt
# Replace the [name] placeholder with the actual name.
# Save the letters in the folder "ReadyToSend".

# Hint1: This method will help you: https://www.w3schools.com/python/ref_file_readlines.asp
# Hint2: This method will also help you: https://www.w3schools.com/python/ref_string_replace.asp
# Hint3: THis method will help you: https://www.w3schools.com/python/ref_string_strip.asp

import os

NAMES_FILE = "./Input/Names/invited_names.txt"
STARTING_LETTER = "./Input/Letters/starting_letter.txt"
OUTPUT_LOCATION = "./Output/ReadyToSend/"
PLACEHOLDER = "[name]"


def read_names():
    """Read the names from a provided file."""
    with open(NAMES_FILE) as f:
        names = [line.strip() for line in f.readlines()]

    return names


def read_starting_letter():
    """Read the template letter."""
    with open(STARTING_LETTER) as f:
        letter = f.read()

    return letter


def insert_name(name, letter: str):
    """Insert the name into the letter."""
    return letter.replace(PLACEHOLDER, name)


def write_letter(letter: str, path):
    """Write the letter to a preset location."""
    with open(path, "w") as f:
        f.write(letter)


if __name__ == "__main__":
    names = read_names()
    letter = read_starting_letter()

    for name in names:
        named_letter = insert_name(name, letter)
        output_path = os.path.join(OUTPUT_LOCATION, f"letter_for_{name}.txt")
        write_letter(named_letter, output_path)
