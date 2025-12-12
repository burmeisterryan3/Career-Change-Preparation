import re

with open("../data/regex15.txt") as f:
    data = f.read().split("\n")

p = re.compile(r"^foo.*")
print(list(filter(p.search, data)))

# OR - match applies the regex to the beginning of the string
p = re.compile(r"foo.*")
print(list(filter(p.match, data)))
