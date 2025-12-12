"""Defines the Snake class for the Snake game."""

import turtle as t

import constants as c


class Snake:
    """Snake class."""

    def __init__(self):
        """Set the initial snake pixels on the screen and define attributes."""
        self.body = []
        self.direction = c.RIGHT
        self._create_snake()
        self.head = self.body[0]

    def _create_snake(self):
        for position in c.STARTING_POSITIONS:
            self._add_part(position)

    def _add_part(self, position):
        """Add a new part to the snake."""
        part = t.Turtle(shape="square")
        part.penup()
        part.color("white")
        part.goto(position)

        self.body.append(part)

    def extend(self):
        """Add a new body part to the end of the snake."""
        self._add_part(self.body[-1].position())

    def reset(self):
        """Reset the snake."""
        for part in self.body:
            part.goto(1000, 1000)

        self.body.clear()
        self._create_snake()
        self.head = self.body[0]

    def move(self):
        """Moves the snake for one complete turn."""
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].goto(self.body[i - 1].position())

        self.head.forward(c.MOVE_DISTANCE)

    def up(self):
        """Moves the snake upward as long as it isn't moving downward."""
        if self.head.heading() != c.DOWN:
            self.head.setheading(c.UP)

    def down(self):
        """Moves the snake downward as long as it isn't moving upward."""
        if self.head.heading() != c.UP:
            self.head.setheading(c.DOWN)

    def left(self):
        """Moves the snake left as long as it isn't moving right."""
        if self.head.heading() != c.RIGHT:
            self.head.setheading(c.LEFT)

    def right(self):
        """Moves the snake right as long as it isn't moving left."""
        if self.head.heading() != c.LEFT:
            self.head.setheading(c.RIGHT)
