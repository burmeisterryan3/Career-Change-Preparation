import re

with open("../data/email_exercise.txt") as f:
    data = f.read().splitlines()

p = re.compile(r"^[a-zA-Z]+[a-zA-Z0-9]*([-._][a-zA-Z0-9]+)*@[a-z]+\.[a-z]{2,}$")
print(list(filter(p.search, data)))
