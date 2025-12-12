import re

with open("../data/regex01.txt") as f:
    data = f.read()

p = re.compile("fooa*bar")
print(p.findall(data))
