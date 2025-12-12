"""Main executor of the pong game."""

import time
from turtle import Screen

import constants as c
from ball import Ball
from paddle import Paddle
from scoreboard import Scoreboard


def setup_screen():
    """Sets the screen to the base starting condition."""
    screen = Screen()
    screen.setup(width=c.WIDTH, height=c.HEIGHT)
    screen.bgcolor("black")
    screen.title("Pong")

    # To allow for smooth animations, refresh the screen after one complete turn
    screen.tracer(0)

    return screen


def bind_right_keys(screen, paddle):
    """Bind the keys to methods in the paddles class for the right paddle."""
    screen.onkeypress(fun=paddle.move_up, key="Up")
    screen.onkeypress(fun=paddle.move_down, key="Down")


def bind_left_keys(screen, paddle):
    """Bind the keys to methods in the paddles class for the left paddle."""
    screen.onkeypress(fun=paddle.move_up, key="w")
    screen.onkeypress(fun=paddle.move_down, key="s")


if __name__ == "__main__":
    screen = setup_screen()
    r_paddle = Paddle()
    l_paddle = Paddle(is_right=False)
    ball = Ball()
    scoreboard = Scoreboard()

    screen.listen()
    bind_right_keys(screen, r_paddle)
    bind_left_keys(screen, l_paddle)

    game_over = False
    in_bounds = True
    while not game_over:
        time.sleep(ball.move_speed)
        screen.update()
        ball.move()

        # Detect collision with the top or bottom walls
        if ball.ycor() > 270 or ball.ycor() < -270:
            ball.y_bounce()

        # Detect collision with a paddle
        if in_bounds and (
            (ball.xcor() > 320 and ball.distance(r_paddle) < 50)
            or (ball.xcor() < -320 and ball.distance(l_paddle) < 50)
        ):
            ball.x_bounce()
        elif ball.xcor() > 340 or ball.xcor() < -340:
            # Detect when the ball goes out of bounds & allow for animation to the boundary
            in_bounds = False
            if ball.xcor() > 400:
                scoreboard.l_point()
                ball.reset_position()
                in_bounds = True
            elif ball.xcor() < -400:
                scoreboard.r_point()
                ball.reset_position()
                in_bounds = True

        if scoreboard.l_score == 10 or scoreboard.r_score == 10:
            game_over = True

    scoreboard.declare_winner()

    screen.exitonclick()
