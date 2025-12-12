import re

with open("../data/regex30.txt") as f:
    data = f.read().splitlines()

print(
    list(
        map(
            lambda x: re.sub(r"\(([0-9]{3})\)(\.[0-9]{3}\.[0-9]{4})", r"\1\2", x),
            data,
        )
    )
)
