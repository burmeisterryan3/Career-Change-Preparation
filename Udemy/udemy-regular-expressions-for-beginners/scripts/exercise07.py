import re

with open("../data/regex07.txt") as f:
    data = f.read()

p = re.compile(r"[^mh]oo")
print(p.findall(data))
