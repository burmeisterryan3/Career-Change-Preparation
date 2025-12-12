import re

with open("../data/regex21.txt") as f:
    data = f.read().splitlines()

# ha repeated at most 2x
p = re.compile(r"^(ha){,2}$")
print(list(filter(p.search, data)))

# NOTE: Without the anchors, ha repeated any number of times will match
# p = re.compile(r"(ha){,2}")
# print(list(filter(p.search, data)))
