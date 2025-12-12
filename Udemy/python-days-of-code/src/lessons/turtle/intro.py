"""Lesson challenges."""

import random
import turtle as t
from turtle import Screen, Turtle

COLORS = [
    "CornflowerBlue",
    "DarkOrchid",
    "IndianRed",
    "DeepSkyBlue",
    "LightSeaGreen",
    "wheat",
    "SlateGray",
    "SeaGreen",
]


def random_color():
    """Return a random color."""
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)

    return (r, g, b)


def challenge_1():
    """Draw a square."""
    tim = Turtle()
    for _ in range(4):
        tim.forward(100)
        tim.left(90)


def challenge_2():
    """Draw a dashed line."""
    tim = Turtle()
    for _ in range(10):
        tim.forward(10)
        tim.up()
        tim.forward(10)
        tim.down()


def __init_high(t):
    t.up()
    t.left(90)
    t.forward(100)
    t.right(90)
    t.down()


def challenge_3():
    """Draw multiple shapes."""
    tim = Turtle()
    side_length = 100
    __init_high(tim)

    for sides in range(3, 11):
        angle = 360 / sides
        tim.color(random.choice(COLORS))

        for side in range(sides + 1):
            if side == 0:
                tim.forward(side_length / 2)
            elif side == sides:
                tim.forward(side_length / 2)
                break
            else:
                tim.forward(side_length)
            tim.right(angle)


def challenge_4(rand=False):
    """Draw a random walk."""
    tim = Turtle()
    tim.hideturtle()

    walk_length = 20
    thickness = 10
    directions = [0, 90, 180, 270]

    tim.width(thickness)
    tim.speed("fastest")

    for _ in range(400):
        if rand:
            tim.color(random_color())
        else:
            tim.color(random.choice(COLORS))

        tim.setheading(random.choice(directions))
        tim.forward(walk_length)


def challenge_5():
    """Random walk wth random colors."""
    t.colormode(255)
    challenge_4(rand=True)


def test():
    """Miscellaneous tests."""
    tim = Turtle("turtle")
    t2 = Turtle("square")
    t2.shapesize(stretch_wid=1, stretch_len=2)
    print(tim.shapesize())
    print(t2.shapesize())


if __name__ == "__main__":
    test()

    screen = Screen()
    screen.exitonclick()
