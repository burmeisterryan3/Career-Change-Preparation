"""File to demonstrate how args & kwargs function."""


# *args - * operator aggregates all the arguments into a tuple
def add(*args):
    """Add all the elements of a set of inputs."""
    # print(type(args))
    return sum(args)


if __name__ == "__main__":
    print(add(2, 3, 4, 5))
