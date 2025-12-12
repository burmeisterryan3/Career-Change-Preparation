"""The paddle object for the pong game."""

from turtle import Turtle

import constants as c


class Paddle(Turtle):
    """Paddle class."""

    def __init__(self, is_right=True):
        """Set the initial paddle pixels on the screen and define attributes."""
        super().__init__()
        self.shape("square")
        self.color("white")
        self.shapesize(stretch_wid=5, stretch_len=1)
        self.penup()
        if is_right:
            self.goto(c.RIGHT_START_POS)
        else:
            self.goto(c.LEFT_START_POS)

    def move_up(self):
        """Move the paddle up."""
        if self.ycor() < 240:
            self.goto(self.xcor(), self.ycor() + c.MOVE_DISTANCE)

    def move_down(self):
        """Move the paddle down."""
        if self.ycor() > -240:
            self.goto(self.xcor(), self.ycor() - c.MOVE_DISTANCE)
