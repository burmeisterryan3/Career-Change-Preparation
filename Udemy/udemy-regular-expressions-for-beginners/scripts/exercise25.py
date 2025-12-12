import re

with open("../data/regex25.txt") as f:
    data = f.read().splitlines()

print(list(map(lambda x: re.sub(r"([0-9]+)x([0-9]+)", r"\1 pix by \2 pix", x), data)))

# OR
# print(
#     list(
#         map(lambda x: re.sub(r"([0-9]+)x([0-9]+)", r"\g<1> pix by \g<2> pix", x), data)
#     )
# )
