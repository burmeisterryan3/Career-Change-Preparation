"""Read and write from files."""

with open("days_of_code/lessons/text/my_file.txt") as file:
    contents = file.read()
    print(contents)

# Overwrite file
# with open("days_of_code/lessons/text/new_file.txt", mode="w") as file:
#     file.write("New text.")

# Append file
with open("days_of_code/lessons/text/new_file.txt", mode="a") as file:
    file.write("New text.")
