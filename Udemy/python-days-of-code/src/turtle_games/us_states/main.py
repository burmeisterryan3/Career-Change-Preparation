"""A game to learn the state names and geography of the US."""

import turtle as t

import pandas as pd

IMG_FILE = "./days_of_code/turtle_games/us_states/blank_states_img.gif"
STATE_FILE = "./days_of_code/turtle_games/us_states/50_states.csv"
OUTPUT_FILE = "./days_of_code/turtle_games/us_states/remaining_states.csv"


def initialize_screen() -> t.Screen:
    """Initialize the screen."""
    screen = t.Screen()

    image = IMG_FILE
    screen.addshape(image)
    t.shape(image)

    return screen


def get_state_data():
    """Read the state data from the csv."""
    return pd.read_csv(STATE_FILE)


def update_title(screen, score):
    """Update the title of the screen."""
    screen.title(f"{score}/50    U.S. States Game")


def add_state():
    """Add a state name to the map."""
    turtle = t.Turtle(visible=False)
    turtle.penup()

    matched = state_df[state_df["state"] == answer_state]

    turtle.goto(matched["x"].values[0], matched["y"].values[0])
    turtle.write(answer_state)


def display_winning_message(screen, score):
    """Display the winning message to the user."""
    update_title(screen, score)
    t.TK.messagebox.showinfo(
        title="You win!",
        message="Congratulations! You guessed all 50 states!",
    )


def exit_game(states):
    """Display a message and write the remaining states to a file."""
    df = pd.DataFrame(states, columns=["state"])
    df.to_csv(OUTPUT_FILE)

    t.TK.messagebox.showinfo(
        title="See you next time",
        message="Good try! Thanks for playing!",
    )


if __name__ == "__main__":
    screen = initialize_screen()
    state_df = get_state_data()
    states = state_df["state"].to_list()
    score = 0
    answer_state = None

    # Set up the exit mechanism
    screen.listen()
    screen.onkey(t.bye, "Escape")  # Press 'Escape' key to close the window

    while states != [] and answer_state != "Exit":
        update_title(screen, score)
        answer_state = screen.textinput(
            title="Guess a State", prompt="What's another state name?"
        )

        if answer_state is None:
            continue
        else:
            answer_state = answer_state.title()

        if answer_state in states:
            add_state()
            score += 1
            states.remove(answer_state)

    if answer_state == "Exit":
        exit_game(states)
    else:
        display_winning_message(screen, score)

    screen.exitonclick()
