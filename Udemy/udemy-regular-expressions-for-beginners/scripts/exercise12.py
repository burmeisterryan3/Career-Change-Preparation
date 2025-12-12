import re

with open("../data/regex12.txt") as f:
    data = f.read()

p = re.compile(r"x+[.:#]y+")
print(p.findall(data))
