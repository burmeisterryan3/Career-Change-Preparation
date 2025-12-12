import re

with open("../data/regex29.txt") as f:
    data = f.read().splitlines()

print(
    list(
        map(
            lambda x: re.sub(
                r"([a-zA-Z]{3})\s([0-9]{1,2})[a-z]{2}\s[0-9]{2}([0-9]{2})",
                r"\2-\1-\3",
                x,
            ),
            data,
        )
    )
)
