import re

with open("../data/regex26.txt") as f:
    data = f.read().splitlines()

print(list(map(lambda x: re.sub(r"([a-zA-Z]+)\s([a-zA-Z]+)", r"\2,\1", x), data)))
