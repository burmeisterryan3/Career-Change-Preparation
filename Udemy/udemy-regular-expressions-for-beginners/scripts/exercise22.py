import re

with open("../data/regex22.txt") as f:
    data = f.read().splitlines()

p = re.compile(r"fooa+bar")
print(list(filter(p.search, data)))
