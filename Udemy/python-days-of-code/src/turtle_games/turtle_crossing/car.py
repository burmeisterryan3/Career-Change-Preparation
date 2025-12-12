"""A class that defines the car for the Turtle Crossing game."""

import random
from turtle import Turtle

import constants as c


class Car(Turtle):
    """Car class."""

    def __init__(self, is_start=True):
        """Inherit and define initial attributes."""
        super().__init__()
        self.shape("square")
        self.penup()
        self.color(random.choice(c.COLORS))
        self.shapesize(stretch_wid=1, stretch_len=2)
        self.setheading(180)
        self.goto(self.gen_x(is_start), self.gen_y())

    def gen_x(self, is_start=True):
        """Get a random x-coordinate."""
        if is_start:
            x = random.randint(*c.START_RANGE)
        else:
            x = c.WIDTH / 2 - 20

        return x

    def gen_y(self):
        """Get a random y-coordinate."""
        y = random.randint(*c.START_RANGE)
        y -= 20 - (y % 20)
        if y < -210:
            y += c.MOVE_DISTANCE
        return y

    def reset_to_start(self):
        """Reset the car to the right side of the screen, to the start."""
        self.goto((c.WIDTH / 2 - 20, random.randint(*c.START_RANGE)))
