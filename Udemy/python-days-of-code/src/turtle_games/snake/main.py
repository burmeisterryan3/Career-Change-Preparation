"""Implements the Snake game."""

import time
from turtle import Screen

import constants as c
from food import Food
from scoreboard import Scoreboard
from snake import Snake


def setup_screen():
    """Sets the screen to the base starting condition."""
    screen = Screen()
    screen.setup(width=c.WIDTH, height=c.HEIGHT)
    screen.bgcolor("black")
    screen.title("Snake")

    # To allow for smooth animations, refresh the screen after one complete turn
    screen.tracer(0)

    return screen


def bind_keys(screen, snake):
    """Bind the keys to methods in the snake class."""
    screen.onkey(fun=snake.up, key="Up")
    screen.onkey(fun=snake.down, key="Down")
    screen.onkey(fun=snake.left, key="Left")
    screen.onkey(fun=snake.right, key="Right")


def near_boundary(snake):
    """Check if the snake is too close to the boundary."""
    return (
        snake.head.xcor() > c.MAX_POS
        or snake.head.xcor() < c.MIN_POS
        or snake.head.ycor() > c.MAX_POS
        or snake.head.ycor() < c.MIN_POS
    )


if __name__ == "__main__":
    screen = setup_screen()
    snake = Snake()
    food = Food()
    scoreboard = Scoreboard()

    screen.listen()
    bind_keys(screen, snake)

    game_over = False
    while not game_over:
        screen.update()
        time.sleep(0.2)
        snake.move()

        # Detect collision with food
        if snake.head.distance(food) < 15:
            food.refresh()
            scoreboard.increase_score()
            snake.extend()

        # Detect collision with wall
        if near_boundary(snake):
            scoreboard.reset()
            snake.reset()

        # Detect collision with tail
        for part in snake.body[1:]:
            if snake.head.distance(part) < 10:
                scoreboard.reset()
                snake.reset()

    screen.exitonclick()
