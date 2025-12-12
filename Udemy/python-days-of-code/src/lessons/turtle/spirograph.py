"""Draw a spirograph."""

import random
import turtle as t

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


def draw_circle_spirograph(turtle, radius=100, tilt=10):
    """Draws a circle spirograph."""
    for _ in range(int(360 / tilt)):
        turtle.color(random.choice(COLORS))
        turtle.circle(radius)
        turtle.setheading(turtle.heading() + tilt)


if __name__ == "__main__":
    tim = t.Turtle()
    tim.hideturtle()
    tim.speed(15)
    draw_circle_spirograph(tim)

    screen = t.Screen()
    screen.exitonclick()
