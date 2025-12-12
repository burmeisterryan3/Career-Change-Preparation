"""Day 8. Implements Caeser Cipher Algorithm."""

from typing import Literal

from pydantic import NonNegativeInt

# fmt: off
LOGO = r"""           
 ,adPPYba, ,adPPYYba,  ,adPPYba, ,adPPYba, ,adPPYYba, 8b,dPPYba,  
a8"     "" ""     `Y8 a8P_____88 I8[   "" ""     `Y8 88P'   "Y8  
8b         ,adPPPPP88 8PP"" "" "  `"Y8ba,  ,adPPPPP88 88          
"8a,   ,aa 88,    ,88 "8b,   ,aa aa    ]8I 88,    ,88 88          
 `"Ybbd8"' `"8bbdP"Y8  `"Ybbd8"' `"YbbdP"' `"8bbdP"Y8 88   
           88             88                                 
           ""             88                                 
                          88                                 
 ,adPPYba, 88 8b,dPPYba,  88,dPPYba,   ,adPPYba, 8b,dPPYba,  
a8"     "" 88 88P'    "8a 88P'    "8a a8P_____88 88P'   "Y8  
8b         88 88       d8 88       88 8PP"" "" " 88          
"8a,   ,aa 88 88b,   ,a8" 88       88 "8b,   ,aa 88          
 `"Ybbd8"' 88 88`YbbdP"'  88       88  `"Ybbd8"' 88          
              88                                             
              88           
"""
# fmt: on

ALPHABET = [
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
]


def caesar(
    text: str,
    shift: NonNegativeInt,
    direction: str = Literal["encode", "decode"],
) -> str:
    """Return the cipher text of plain text shifted by shift letters."""
    new_text = ""

    if direction == "decode":
        shift *= -1

    for char in text.lower():
        if char.isalpha():
            # % 25 due to 0-indexing
            new_text += ALPHABET[(ALPHABET.index(char) + shift) % 25]
        else:  # Non-alphabetic character
            new_text += char

    return new_text


def is_int(s: str):
    """Check if string is a digit."""
    if s[0] in ("-", "+"):
        return s[1:].isdigit()
    return s.isdigit()


if __name__ == "__main__":
    print(f"{LOGO}\n\n")

    keep_going = "y"
    while keep_going == "y":
        direction = ""
        while direction != "encode" and direction != "decode":
            direction = input(
                "Type 'encode' to encrypt, type 'decode' to decrypt:\n"
            )

        text = input("Type your message:\n").lower()

        shift = "-1"
        while not is_int(shift) or int(shift) < 0:
            shift = input("Type the shift number:\n")
        shift = int(shift)

        text = caesar(text, shift, direction)
        print(f"The {direction}d text is {text}")

        keep_going = input(
            'Continue to encode or decode another phrase or word? "Y" or "N"? '
        ).lower()

    print("\nGoodbye\n")
