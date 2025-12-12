import re

with open("../data/regex04.txt") as f:
    data = f.read()

p = re.compile("foo\s*bar")
print(p.findall(data))
