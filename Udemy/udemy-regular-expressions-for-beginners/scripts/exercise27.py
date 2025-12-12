import re

with open("../data/regex27.txt") as f:
    data = f.read().splitlines()

print(
    list(
        map(
            lambda x: re.sub(r"(11|12|[1-9]):([0-5][0-9])", r"\2 mins past \1", x), data
        )
    )
)

# Solution from course... not as specific
print(
    list(map(lambda x: re.sub(r"([0-9]{1,2}):([0-9]{2})", r"\2 mins past \1", x), data))
)
