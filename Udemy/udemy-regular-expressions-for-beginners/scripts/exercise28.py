import re

with open("../data/regex28.txt") as f:
    data = f.read().splitlines()

print(
    list(
        map(lambda x: re.sub(r"[0-9]{3}\.[0-9]{3}\.([0-9]{4})", r"xxx.xxx.\1", x), data)
    )
)
