import re

with open("../data/regex20.txt") as f:
    data = f.read().splitlines()

# ha repeated at least 4x
p = re.compile(r"(ha){4,}")
print(list(filter(p.search, data)))
