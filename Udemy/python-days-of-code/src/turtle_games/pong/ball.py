"""The ball class for the pong game."""

from turtle import Turtle


class Ball(Turtle):
    """Ball class."""

    def __init__(self):
        """Initialize attributes."""
        super().__init__()
        self.shape("circle")
        self.color("white")
        self.penup()
        self.x_move = 10
        self.y_move = 10
        self.move_speed = 0.1

    def reset_position(self):
        """Reset the ball to the middle of the board."""
        self.goto(0, 0)
        self.move_speed = 0.1
        self.x_bounce()

    def move(self):
        """Move the ball."""
        self.goto(
            self.xcor() + self.x_move,
            self.ycor() + self.y_move,
        )

    def y_bounce(self):
        """Change the direction of the ball due to a collision with a wall."""
        self.y_move *= -1

    def x_bounce(self):
        """Change the direction of the ball due to a collision with a paddle."""
        self.x_move *= -1
        self.move_speed *= 0.9
