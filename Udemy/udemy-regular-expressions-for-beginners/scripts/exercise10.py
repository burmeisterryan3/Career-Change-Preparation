import re

with open("../data/regex10.txt") as f:
    data = f.read()

p = re.compile(r"[j-mJ-Mz]oo")
print(p.findall(data))
