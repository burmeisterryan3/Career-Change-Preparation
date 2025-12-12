"""Defines the Food class for the Snake game."""

from turtle import Turtle

import constants as c


class Scoreboard(Turtle):
    """Scoreboard class."""

    def __init__(self):
        """Initialize attributes."""
        super().__init__()
        self.hideturtle()
        self.color("white")
        self.penup()
        self.speed("fastest")
        self.goto(c.SCORE_POSITION)
        self.score = 0
        with open("days_of_code/turtle_games/snake/high_score.txt") as f:
            self.high_score = int(f.read())
        self._update_scoreboard()

    def _update_scoreboard(self):
        """Update the scoreboard."""
        self.clear()
        self.write(
            f"Score: {self.score} High Score: {self.high_score}",
            align=c.ALIGNMENT,
            font=c.FONT,
        )

    def increase_score(self):
        """Update the score."""
        self.score += 1
        self._update_scoreboard()

    def reset(self):
        """Reset the score."""
        if self.score > self.high_score:
            self.high_score = self.score
            with open(
                "days_of_code/turtle_games/snake/high_score.txt", "w"
            ) as f:
                f.write(f"{self.high_score}")
        self.score = 0
        self._update_scoreboard()

    def game_over(self):
        """Notify the player that the game is over."""
        self.goto(0, 0)
        self.write("GAME OVER", align=c.ALIGNMENT, font=c.FONT)
