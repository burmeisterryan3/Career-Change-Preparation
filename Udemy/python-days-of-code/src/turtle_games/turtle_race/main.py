"""Simulate a race of turtle using the Turtle library."""

import random
import turtle as t

# Define constants
HEIGHT = 400
WIDTH = 500
FINISHING_LINE = 230
COLORS = ["red", "orange", "yellow", "green", "blue", "purple"]


def setup_screen(screen):
    """Set the screen size."""
    screen.setup(height=HEIGHT, width=WIDTH)
    screen.title("Turtle Race!")


def place_turtles(colors):
    """Place all the turtles on the starting line."""
    y_buffer = 60
    x_buffer = 20

    # All turtles should be separated equally in the y-dimension
    first_y = (-1 * HEIGHT / 2) + y_buffer
    separation = (HEIGHT - y_buffer * 2) / (len(colors) - 1)
    y_positions = [first_y + i * separation for i in range(len(colors))]

    # All turtles will start at the same x
    x_start = (-WIDTH / 2) + x_buffer

    turtles = []
    for color, y_start in zip(colors, y_positions):
        turtle = t.Turtle(shape="turtle")
        turtle.penup()
        turtle.color(color)
        turtle.goto(x=x_start, y=y_start)
        turtles.append(turtle)

    return turtles


def guess_winner(screen, title=None, prompt=None):
    """Make a prediction as to which turtle will win."""
    if title is None:
        title = "Make your bet"
    if prompt is None:
        prompt = "Which turtle will win? Enter a color: "

    bet = screen.textinput(title=title, prompt=prompt)
    while bet not in COLORS and bet not in [c[0] for c in COLORS]:
        bet = screen.textinput(
            title="Invalid input!",
            prompt=f"Which turtle will win? Enter one of the following: {', '.join(COLORS)}",
        )

    return bet


def take_turn(turtles):
    """Take a turn. Each turtle will move between 0 & 10 spaces."""
    steps = random.sample(list(range(11)), len(turtles))

    winner = None
    for turtle, step in zip(turtles, steps):
        turtle.setx(turtle.position()[0] + step)

        if turtle.position()[0] >= FINISHING_LINE:
            winner = turtle
            break

    return winner


if __name__ == "__main__":
    keep_playing = "Y"
    screen = t.Screen()
    setup_screen(screen)

    while keep_playing.upper() == "Y":
        screen.clearscreen()
        turtles = place_turtles(colors=COLORS)

        user_bet = guess_winner(screen)

        winner = None
        while winner is None:
            winner = take_turn(turtles)

        title = f"{winner.color()[1].capitalize()} wins!"
        if winner.color()[1] == user_bet or winner.color()[1][0] == user_bet:
            keep_playing = screen.textinput(
                title=title,
                prompt="Great guess! Your turtle won! Play again? [Y]es or [N]o",
            )
        else:
            keep_playing = screen.textinput(
                title=title,
                prompt="Oh no! Your turtle lost! Play again? [Y]es or [N]o",
            )

    t.TK.messagebox.showinfo(
        title="Good bye!", message="Thanks for playing! Come again soon."
    )

    screen.exitonclick()
