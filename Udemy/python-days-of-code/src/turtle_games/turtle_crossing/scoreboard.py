"""Defines the Food class for the Turtle Crossing game."""

from turtle import Turtle

import constants as c


class Scoreboard(Turtle):
    """Scoreboard class."""

    def __init__(self):
        """Initialize attributes."""
        super().__init__()
        self.hideturtle()
        self.color("black")
        self.penup()
        self.speed("fastest")
        self.goto(c.SCORE_POSITION)
        self.level = 1
        self._update_scoreboard()

    def _update_scoreboard(self):
        """Update the scoreboard."""
        self.write(f"Level: {self.level}", align=c.ALIGNMENT, font=c.FONT)

    def increase_level(self):
        """Update the level."""
        self.level += 1
        self.clear()
        self._update_scoreboard()

    def game_over(self):
        """Notify the player that the game is over."""
        self.goto(0, 0)
        self.write("GAME OVER", align=c.ALIGNMENT, font=c.FONT)
