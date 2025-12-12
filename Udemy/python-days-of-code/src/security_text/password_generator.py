"""Day 5."""

import random

letters = [
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
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "X",
    "Y",
    "Z",
]
numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
symbols = ["!", "#", "$", "%", "&", "(", ")", "*", "+"]

print("Welcome to the PyPassword Generator!")
nr_letters = int(input("How many letters would you like in your password?\n"))
nr_symbols = int(input("How many symbols would you like?\n"))
nr_numbers = int(input("How many numbers would you like?\n"))

# In addition to the below, you can also run a for loop over each type followed by random.shuffle

password = ""
letter_acc, symbol_acc, number_acc = 0, 0, 0
while len(password) < nr_letters + nr_symbols + nr_numbers:
    next_sym_type = random.randrange(3)

    if next_sym_type == 0 and letter_acc < nr_letters:
        password += random.choice(letters)
        letter_acc += 1
    elif next_sym_type == 1 and number_acc < nr_numbers:
        password += random.choice(numbers)
        number_acc += 1
    elif symbol_acc < nr_symbols:
        password += random.choice(symbols)
        symbol_acc += 1

print(password)
