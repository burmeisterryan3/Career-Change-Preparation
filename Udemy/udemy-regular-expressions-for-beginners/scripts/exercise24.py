import re

with open("../data/regex24.txt") as f:
    data = f.read().splitlines()

p = re.compile(r"(log|ply)wood")
print(list(filter(p.search, data)))
