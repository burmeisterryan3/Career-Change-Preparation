import re

with open("../data/regex19.txt") as f:
    data = f.read().split("\n")

# a-z repeated between 4-6 times
p = re.compile(r"^[a-z]{4,6}$")
print(list(filter(p.search, data)))
