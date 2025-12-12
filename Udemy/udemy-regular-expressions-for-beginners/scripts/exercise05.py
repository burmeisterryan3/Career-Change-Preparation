import re

with open("../data/regex05.txt") as f:
    data = f.read()

p = re.compile("[fcl]oo")
print(p.findall(data))
