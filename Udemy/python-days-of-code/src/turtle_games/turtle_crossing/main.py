"""Implements the Turtle Crossing game."""

import time
from turtle import Screen

import constants as c
from car import Car
from crosser import Crosser
from scoreboard import Scoreboard


def setup_screen():
    """Sets the screen to the base starting condition."""
    screen = Screen()
    screen.setup(width=c.WIDTH, height=c.HEIGHT)
    screen.bgcolor("white")
    screen.title("Turtle Crossing")

    # To allow for smooth animations, refresh the screen after one complete turn
    screen.tracer(0)

    return screen


def bind_keys(screen, crosser):
    """Bind the keys to methods in the crosser class."""
    screen.onkeypress(fun=crosser.move_up, key="Up")
    screen.onkeypress(fun=crosser.move_down, key="Down")
    screen.onkeypress(fun=crosser.move_left, key="Left")
    screen.onkeypress(fun=crosser.move_right, key="Right")
    return


def initialize_cars(n_cars=20):
    """Initialize cars on the game board."""
    return [Car() for _ in range(n_cars)]


if __name__ == "__main__":
    screen = setup_screen()
    scoreboard = Scoreboard()
    crosser = Crosser()
    cars = initialize_cars(20 + scoreboard.level)

    screen.listen()
    bind_keys(screen, crosser)

    game_over = False
    game_interval = 0.5
    while not game_over:
        screen.update()

        # Check if at the end of the board
        if crosser.ycor() > 240:
            scoreboard.increase_level()
            crosser.goto(c.CROSSER_START_POSITION)
            game_interval *= 0.9
            cars.append(Car(is_start=False))

        if crosser.ycor() < -240:
            crosser.goto(crosser.xcor(), -220)

        for car in cars:
            # Check for collision with the crosser
            if (
                abs(car.ycor() - crosser.ycor()) < 18
                and abs(car.xcor() - crosser.xcor()) < 30
                and crosser.xcor() - car.xcor() < 30
            ):
                print(
                    f"car.ycor() - crosser.ycor() = {car.ycor() - crosser.ycor()}"
                )
                print(
                    f"car.xcor() - crosser.xcor() = {car.xcor() - crosser.xcor()}"
                )
                game_over = True
                scoreboard.game_over()
                screen.update()
                break
            else:
                car.forward(20)

                # Check if car position needs to reset
                if car.xcor() < -250:
                    car.reset_to_start()

        time.sleep(game_interval)

    screen.exitonclick()
