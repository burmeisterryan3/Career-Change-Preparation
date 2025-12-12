"""Defines the Food class for the Snake game."""

import random
from turtle import Turtle

import constants as c


class Food(Turtle):
    """Food class."""

    def __init__(self):
        """Inherit and define initial attributes."""
        super().__init__()
        self.shape("circle")
        self.penup()
        self.shapesize(stretch_len=0.5, stretch_wid=0.5)
        self.color("blue")
        self.speed("fastest")
        self._set_initial_position()

    def _near_snake_start(self):
        x, y = self.position()
        return (
            x < c.RIGHT_START_BOUNDARY
            and x > c.LEFT_START_BOUNDARY
            and y < c.UP_START_BOUNDARY
            and y > c.DOWN_START_BOUNDARY
        )

    def _set_initial_position(self):
        """Ensure the food is distant from the starting position of the snake."""
        while self._near_snake_start():
            self.refresh()

    def _near_current_pos(self, new_x, new_y):
        cur_x, cur_y = self.position()
        return abs(cur_x - new_x) < 15 or abs(cur_y - new_y) < 15

    def _near_scoreboard(self, x, y):
        return (
            x > c.SCORE_MIN_X
            and x < c.SCORE_MAX_X
            and y > c.SCORE_MIN_Y
            and y < c.SCORE_MAX_Y
        )

    def refresh(self):
        """Move the food to a new location and ensure it is not near the current location."""
        new_x = random.randint(c.MIN_POS, c.MAX_POS)
        new_y = random.randint(c.MIN_POS, c.MAX_POS)

        while self._near_current_pos(new_x, new_y) or self._near_scoreboard(
            new_x, new_y
        ):
            new_x = random.randint(c.MIN_POS, c.MAX_POS)
            new_y = random.randint(c.MIN_POS, c.MAX_POS)

        self.goto((new_x, new_y))
