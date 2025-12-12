"""Utility functions for app.py."""

from blackjack import Blackjack
from hangman import Hangman
from higher_lower import HigherLower
from number_guessing import NumberGuessing
from quiz import Quiz
from rock_paper_scissors import RockPaperScissors

GAMES = [
    Blackjack(),
    Hangman(),
    HigherLower(),
    NumberGuessing(),
    Quiz(),
    RockPaperScissors(),
]
GAMES_INDEX = {
    0: "Blackjack",
    1: "Hangman",
    2: "Higher Lower",
    3: "Number Guessing",
    4: "Quiz",
    5: "Rock Paper Scissors",
}


def print_game_options():
    """Print the games in GAMES."""
    print("Here are the games you can play.")
    for k, v in GAMES_INDEX.items():
        print(f"{k}: {v}")


def get_game():
    """Get the game index of the game the user wants to play."""
    game_index = -1
    while (
        not isinstance(game_index, int)
        or game_index < 0
        or game_index >= len(GAMES)
    ):
        try:
            game_index = int(
                input(
                    "Which game do you want to play? Enter the number of the corresponding game. "
                )
            )
        except ValueError:
            pass

    return GAMES[game_index]
