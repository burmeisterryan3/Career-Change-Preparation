"""Scoreboard for the pong game."""

from turtle import Turtle

import constants as c


class Scoreboard(Turtle):
    """Scoreboard class."""

    def __init__(self):
        """Initialize object attributes."""
        super().__init__()
        self.color("white")
        self.penup()
        self.hideturtle()
        self.r_score = 0
        self.l_score = 0

        self.write_score()

    def write_score(self):
        """Writes the scores."""
        self.clear()
        self.goto(c.L_SCORE_POS)
        self.write(self.l_score, align="center", font=c.FONT)

        self.goto(c.R_SCORE_POS)
        self.write(self.r_score, align="center", font=c.FONT)

    def l_point(self):
        """Add a point to left."""
        self.l_score += 1
        self.write_score()

    def r_point(self):
        """Add a point to left."""
        self.r_score += 1
        self.write_score()

    def declare_winner(self):
        """Declare the winner."""
        if self.r_score > self.l_score:
            winner = "RIGHT"
        else:
            winner = "LEFT"

        self.goto(0, 0)
        self.write(f"{winner} WINS!", align="center", font=c.FONT)
