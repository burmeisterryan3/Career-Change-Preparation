import re

with open("../data/regex23.txt") as f:
    data = f.read().splitlines()

p = re.compile(r"^https?:")
print(list(filter(p.search, data)))
