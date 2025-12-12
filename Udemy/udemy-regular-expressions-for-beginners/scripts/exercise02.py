import re

with open("../data/regex02.txt") as f:
    data = f.read()

p = re.compile("foo.bar")
print(p.findall(data))
