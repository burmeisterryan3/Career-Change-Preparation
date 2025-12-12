import re

with open("../data/regex16.txt") as f:
    data = f.read().split("\n")

p = re.compile(r".*bar$")
print(list(filter(p.search, data)))
