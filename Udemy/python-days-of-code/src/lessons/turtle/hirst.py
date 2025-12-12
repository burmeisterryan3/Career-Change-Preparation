"""Recreate the Hirst dot painting."""

# import os

# import colorgram
import random
import turtle as t

COLORS = [
    (216, 156, 81),
    (128, 165, 206),
    (63, 82, 149),
    (214, 226, 218),
    (175, 81, 35),
    (61, 42, 30),
    (131, 193, 163),
    (214, 170, 26),
    (202, 87, 111),
    (151, 59, 94),
    (235, 84, 36),
    (214, 222, 232),
    (232, 219, 223),
    (225, 207, 108),
    (160, 30, 24),
    (77, 125, 51),
    (45, 54, 124),
    (139, 34, 57),
    (32, 54, 32),
    (190, 126, 160),
    (27, 32, 72),
    (98, 126, 182),
    (228, 178, 167),
    (57, 35, 41),
    (73, 150, 171),
    (107, 84, 16),
    (166, 205, 184),
    (221, 174, 184),
    (165, 200, 209),
    (178, 187, 214),
    (242, 197, 6),
    (44, 75, 42),
    (108, 145, 86),
]


# def extract_colors(pic="hirst.jpg"):
#     """Extract colors from an image and place into a list."""
#     path = os.path.join(
#         os.getcwd(),  # playground
#         "udemy-100-days-of-code-python",
#         "days_of_code",
#         "turtle",
#         pic,
#     )
#     colors = colorgram.extract(path, 81)

#     print([tuple(color.rgb) for color in colors])


def set_starting_position(turtle, n_rows=10, n_cols=10):
    """Move the cursor to the starting position.

    The goal will be to draw a 10x10 grid of circles with dimaeters of 20 units
    and separation of 50 units between circles.

    This results in a 20*10 + 50*9 = 650 units along by the x- and y- axes.

    Given the starting position defaults to (0,0), half of the units should
    occur to the left and the other half to the right. Thus, we should move down
    and left 325 units to start.
    """
    turtle.up()
    turtle.hideturtle()
    turtle.setposition(-325, -325)
    turtle.showturtle()
    turtle.down()


def draw_row(turtle, n_cols=10, diameter=20, separation=50):
    """Draw a row of circles."""
    turtle.hideturtle()
    for col in range(n_cols):  # each column
        turtle.color(random.choice(COLORS))

        turtle.down()
        turtle.begin_fill()
        turtle.circle(diameter)
        turtle.end_fill()
        # turtle.dot(diameter, random.choice(COLORS))
        turtle.up()

        if col != n_cols - 1:
            turtle.forward(separation + diameter)


def reset_row(turtle, n_cols=10, diameter=20, separation=50):
    """Return the cursor to the beginning of the row."""
    turtle.setheading(90)
    # Need to travel the radius of both circles plus the desired separation
    turtle.forward(separation + diameter)
    turtle.setheading(180)
    # -1 due to starting and finishing in the middle of a circle
    turtle.forward((n_cols - 1) * (diameter + separation))
    turtle.setheading(0)


if __name__ == "__main__":
    screen = t.Screen()
    screen.screensize(700, 700)

    # extract_colors()
    tim = t.Turtle()
    tim.speed("fastest")
    t.colormode(255)

    set_starting_position(tim)
    for _ in range(10):  # each row
        draw_row(tim)
        reset_row(tim)

    screen.exitonclick()
    tim.up()
