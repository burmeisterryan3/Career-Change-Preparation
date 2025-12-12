"""Etch a sketch with Turtle."""

import turtle as t

# Declare global variables
tim = t.Turtle()
screen = t.Screen()

is_moving_forward = False
is_moving_backward = False
is_moving_cw = False
is_moving_ccw = False


def move_forward():
    """Move the turtle forward."""
    if is_moving_forward:
        tim.forward(10)
        screen.ontimer(fun=move_forward, t=100)


def start_forward():
    """Move forward and disable the key press event to prevent multiple calls."""
    global is_moving_forward
    is_moving_forward = True
    move_forward()


def stop_forward():
    """Re-enable the key press event."""
    global is_moving_forward
    is_moving_forward = False


def move_backward():
    """Move the turtle backward."""
    if is_moving_backward:
        tim.backward(10)
        screen.ontimer(fun=move_backward, t=100)


def start_backward():
    """Move backward and disable the key press event to prevent multiple calls."""
    global is_moving_backward
    is_moving_backward = True
    move_backward()


def stop_backward():
    """Re-enable the key press event."""
    global is_moving_backward
    is_moving_backward = False


def move_cw():
    """Rotate the turtle clockwise."""
    if is_moving_cw:
        tim.setheading(tim.heading() - 10)
        screen.ontimer(fun=move_cw, t=100)


def start_cw():
    """Move clockwise and disable the key press event to prevent multiple calls."""
    global is_moving_cw
    is_moving_cw = True
    move_cw()


def stop_cw():
    """Re-enable the key press event."""
    global is_moving_cw
    is_moving_cw = False


def move_ccw():
    """Rotate the turtle counter-clockwise."""
    if is_moving_ccw:
        tim.setheading(tim.heading() + 10)
        screen.ontimer(fun=move_ccw, t=100)


def start_ccw():
    """Move counter-clockwise and disable the key press event to prevent multiple calls."""
    global is_moving_ccw
    is_moving_ccw = True
    move_ccw()


def stop_ccw():
    """Re-enable the key press event."""
    global is_moving_ccw
    is_moving_ccw = False


if __name__ == "__main__":
    screen.listen()

    # Bind the key press and key release events
    screen.onkeypress(key="w", fun=start_forward)
    screen.onkeyrelease(key="w", fun=stop_forward)
    screen.onkeypress(key="s", fun=start_backward)
    screen.onkeyrelease(key="s", fun=stop_backward)
    screen.onkeypress(key="d", fun=start_cw)
    screen.onkeyrelease(key="d", fun=stop_cw)
    screen.onkeypress(key="a", fun=start_ccw)
    screen.onkeyrelease(key="a", fun=stop_ccw)

    # Clear and reset the screen when "c" is pressed
    screen.onkey(key="c", fun=screen.resetscreen)

    screen.exitonclick()
