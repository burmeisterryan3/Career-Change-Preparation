"""A class that defines the turtle for the Turtle Crossing game."""

from turtle import Turtle

import constants as c


class Crosser(Turtle):
    """Crosser class."""

    def __init__(self):
        """Inherit and define initial attributes."""
        super().__init__()
        self.shape("turtle")
        self.penup()
        self.color("black")
        self.speed("fastest")
        self.setheading(90)
        self.shapesize(stretch_wid=1, stretch_len=0.75)
        self.goto(*c.CROSSER_START_POSITION)

    def move_up(self):
        """Moves the crosser upward."""
        self.forward(c.MOVE_DISTANCE)

    def move_down(self):
        """Moves the crosser downward."""
        self.backward(c.MOVE_DISTANCE)

    def move_left(self):
        """Moves the crosser left."""
        self.setheading(180)
        self.forward(c.MOVE_DISTANCE)
        self.setheading(90)

    def move_right(self):
        """Moves the crosser right."""
        self.setheading(0)
        self.forward(c.MOVE_DISTANCE)
        self.setheading(90)
