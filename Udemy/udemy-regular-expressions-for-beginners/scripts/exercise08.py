import re

with open("../data/regex08.txt") as f:
    data = f.read()

p = re.compile(r"[j-m]oo")
print(p.findall(data))
