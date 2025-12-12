import re

with open("../data/regex09.txt") as f:
    data = f.read()

p = re.compile(r"[j-mz]oo")
print(p.findall(data))
