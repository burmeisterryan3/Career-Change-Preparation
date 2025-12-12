import re

with open("../data/regex06.txt") as f:
    data = f.read()

p = re.compile(r"[fcdplb]oo")
print(p.findall(data))
