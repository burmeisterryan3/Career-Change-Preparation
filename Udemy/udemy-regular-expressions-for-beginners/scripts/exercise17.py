import re

with open("../data/regex17.txt") as f:
    data = f.read().split("\n")

p = re.compile(r"^foo$")
print(list(filter(p.search, data)))
