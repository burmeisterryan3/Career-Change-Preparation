import re

with open("../data/regex03.txt") as f:
    data = f.read()

p = re.compile("foo.*bar")
print(p.findall(data))
