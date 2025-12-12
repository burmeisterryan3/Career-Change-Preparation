import re

with open("../data/regex14.txt") as f:
    data = f.read()

p = re.compile(r"x+[#^\\]y+")
print(p.findall(data))
