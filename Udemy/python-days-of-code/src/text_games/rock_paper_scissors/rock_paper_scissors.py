"""Day 4."""

import random
from enum import IntEnum
from os import system
from time import sleep

from game import DifficultyEnum, Game, ResultEnum
from pydantic import PrivateAttr

from .logo import LOGO, PAPER, ROCK, SCISSORS


class RPSEnum(IntEnum):
    """Rock, paper, scissors options enum."""

    rock = 0
    paper = 1
    scissors = 2


class RockPaperScissors(Game):
    """Defines the rock, paper, scissors class."""

    _IMAGES: list[str] = PrivateAttr([ROCK, PAPER, SCISSORS])

    def __init__(self):  # noqa: D107
        super().__init__()
        self._difficulty = DifficultyEnum.easy
        self._user_choice: RPSEnum = PrivateAttr
        self._computer_choice: RPSEnum = PrivateAttr

    def _print_logo(self) -> None:
        system("clear")
        print(f"{LOGO}\n\n")

    def _print_welcome(self) -> None:
        """Print welcome message for user."""
        self._print_logo()
        print("Welcome to Rock, Paper, Scissors!")

    def _print_help(self) -> None:
        print()
        print("Select rock, paper, or scissors.")
        print("Rock beats scissors. Scissors beat paper. Paper beats rocks.")
        print()

    def start_playing(self) -> None:
        """Start playing the game."""
        self._print_welcome()

    def _get_user_choice(self) -> int:
        try:
            user_choice = int(
                input(
                    "What do you choose? Type 0 for Rock, 1 for Paper or 2 for scissors: "
                )
            )
            while user_choice not in RPSEnum:
                user_choice = int(
                    input(
                        "Invalid choice! Type 0 for Rock, 1 for Paper or 2 for scissors: "
                    )
                )
        except ValueError:
            self._get_user_choice()

        return user_choice

    def _user_turn(self) -> None:
        """Play a turn of rock, paper, scissors."""
        self._user_choice = self._get_user_choice()
        print(self._IMAGES[self._user_choice])
        sleep(1)  # pause for user to digest update

    def _computer_turn(self) -> None:
        self._computer_choice = RPSEnum(random.randint(0, 2))
        print("Computer chose:")
        print(self._IMAGES[self._computer_choice] + "\n")
        sleep(1)  # pause for user to digest update
        self._result = ResultEnum.finished

    def output_result(self) -> None:
        """Print the result message."""
        loss = "Oh no! You lose!"
        win = "Great job! You win!"
        tie = "Eggghhhh... tie"
        if self._user_choice == RPSEnum.rock:
            if self._computer_choice == RPSEnum.paper:
                print(loss)
                self._result = ResultEnum.loss
            elif self._computer_choice == RPSEnum.rock:
                print(tie)
                self._result = ResultEnum.tie
            else:  # scissors
                print(win)
                self._result = ResultEnum.win
        elif self._user_choice == RPSEnum.paper:
            if self._computer_choice == RPSEnum.scissors:
                print(loss)
                self._result = ResultEnum.loss
            elif self._computer_choice == RPSEnum.paper:
                print(tie)
                self._result = ResultEnum.tie
            else:  # rock
                print(win)
                self._result = ResultEnum.win
        else:  # scissors
            if self._computer_choice == RPSEnum.rock:
                print(loss)
                self._result = ResultEnum.loss
            elif self._computer_choice == RPSEnum.scissors:
                print(tie)
                self._result = ResultEnum.tie
            else:  # paper
                print(win)
                self._result = ResultEnum.win

    def reset(self) -> None:
        """Reset the values for a new game."""
        super().reset()
