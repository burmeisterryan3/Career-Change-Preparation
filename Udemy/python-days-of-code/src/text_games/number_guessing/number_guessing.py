"""Day 12. Number guessing game."""

from os import system
from random import randint

from game import DifficultyEnum, Game, ResultEnum
from pydantic import PrivateAttr

from .logo import logo


class NumberGuessing(Game):
    """Defines the number guessing game class."""

    def __init__(self):  # noqa: D107
        super().__init__()
        self._guesses_remaining: int = PrivateAttr(0)
        self._number_to_guess: int = PrivateAttr(randint(1, 100))
        self._ties_possible = False

    def _print_logo(self):
        system("clear")
        print(f"{logo}\n\n")

    def _print_welcome(self) -> None:
        self._print_logo()
        print("Welcome to the Number Guessing Game!")

    def _print_help(self) -> None:
        print()
        print("Try to guess a random number between 1 and 100.")
        print("Easy - 10 guesses allowed")
        print("Hard - 5 guesses allowed")
        print()

    def start_playing(self) -> None:
        """Print a welcoming message to start the game."""
        self._print_welcome()
        print("I'm thinking of a number between 1 and 100.")

        if self._difficulty == DifficultyEnum.easy:
            self._guesses_remaining = 10
        else:
            self._guesses_remaining = 5

    def _get_guess(self) -> int:
        guess = -1
        while not isinstance(guess, int) or guess < 0 or guess > 100:
            try:
                guess = int(input("Enter a number between 1 and 100: "))
            except ValueError:
                print("Invalid input!")

        return guess

    def _user_turn(self):
        guess = self._get_guess()
        if guess < self._number_to_guess:
            print("Too low... Guess again!")
            self._guesses_remaining -= 1
        elif guess > self._number_to_guess:
            print("Too high... Guess again!")
            self._guesses_remaining -= 1
        else:
            self._result = ResultEnum.win

        if self._guesses_remaining == 0:
            self._result = ResultEnum.loss
        else:
            print(f"You have {self._guesses_remaining} guesses left.")

    def _computer_turn(self):
        pass

    def output_result(self) -> None:
        """Outputs the result of the game."""
        if self._result == ResultEnum.win:
            print("You got it!")
        else:
            print("Oh no! You've run out of guesses.")

        print(f"The number was {self._number_to_guess}.")

    def reset(self) -> None:
        """Reset the values for a new game."""
        super().reset()
        self._number_to_guess = randint(1, 100)
