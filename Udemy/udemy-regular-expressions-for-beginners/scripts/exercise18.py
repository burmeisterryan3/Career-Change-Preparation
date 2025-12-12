import re

with open("../data/regex18.txt") as f:
    data = f.read().split("\n")

p = re.compile(r"^[0-9][0-9][0-9]$")
print(list(filter(p.search, data)))

p = re.compile(r"^[0-9]{3}$")
print(list(filter(p.search, data)))
