"""Day 7. Prepares all the necessary modules in order to play hangman."""

from __future__ import annotations

import random
from os import system

from game import DifficultyEnum, Game, ResultEnum
from pydantic import NonNegativeInt, PrivateAttr

from .utils import EASY, HARD, LOGO, STAGES


class Hangman(Game):
    """Define the hangman class."""

    _MAX_STARTING_LIVES: int = PrivateAttr(6)

    def __init__(self):  # noqa: D107
        super().__init__()
        self._word_to_guess: str = PrivateAttr
        self._letters_remaining: NonNegativeInt = PrivateAttr
        self._previous_guesses: list[str] = PrivateAttr
        self._lives_remaining: NonNegativeInt = PrivateAttr(
            Hangman._MAX_STARTING_LIVES
        )
        self._ties_possible = False

    def _print_logo(self) -> None:
        system("clear")
        print(f"{LOGO}\n\n")

    def _print_welcome(self) -> None:
        self._print_logo()
        print("Welcome to Hangman, the ultimate word guessing game!")

    def _print_help(self) -> None:
        print()
        print("Guess letters one at a time to fill in the blanks.")
        print("Guess the word in less than 6 guesses to win!")
        print()

    def start_playing(self) -> None:
        """Start the game with a welcome."""
        self._print_welcome()

        if self.difficulty == DifficultyEnum.easy:
            self._word_to_guess = random.choice(EASY).lower()
        else:
            self._word_to_guess = random.choice(HARD).lower()

        self._letters_remaining = len(self._word_to_guess)
        self._guessed_status = ["_"] * len(self._word_to_guess)
        self._previous_guesses = []

    def _print_turn_start(self) -> None:
        print(f"\n{' '.join(self._guessed_status)}")
        print(f"{STAGES[self._lives_remaining]}\n")

    def _get_guess(self) -> str:
        while True:
            guess = input("Guess a letter? ").lower()

            if not guess.isalpha():
                print(f"{guess} isn't a letter!")
            elif len(guess) > 1:
                print(f"You guessed {guess}... that's more than one letter!")
            elif guess in self._previous_guesses:
                print(f"You've already guessed {guess}!")
            else:
                break

        self._previous_guesses.append(guess)
        return guess

    def _update_guessed_status(self, guess: str) -> int:
        """Update the locations where the guessed letter is within word."""
        num_updates = 0
        for i, char in enumerate(self._word_to_guess):
            if guess == char:
                self._guessed_status[i] = guess
                num_updates += 1

        return num_updates

    def _user_turn(self) -> None:
        """Take a turn."""
        self._print_turn_start()
        guess = self._get_guess()
        num_updates = self._update_guessed_status(guess)

        if num_updates == 0:
            print("\nOh no! The letter you guessed wasn't in the word!")
            self._lives_remaining -= 1
        else:
            print("\nGreat guess! Your letter was in the word!")
            self._letters_remaining -= num_updates

        if self._letters_remaining == 0:
            self._result = ResultEnum.win
        elif self._lives_remaining == 0:
            self._result = ResultEnum.loss

    def _computer_turn(self) -> None:
        """No computer actions. Pass."""
        pass

    def output_result(self) -> None:
        """Print the final result."""
        if self._lives_remaining > 0:
            print(f'\nYou guessed it! The word was "{self._word_to_guess}".')
            print("You win!\n")
        else:
            print("\nOh no! You're out of guesses!")
            print(f"{STAGES[self._lives_remaining]}\n")
            print(f'The word was "{self._word_to_guess}".')
            print("You lose!\n")

    def reset(self) -> None:
        """Reset values for a new game."""
        super().reset()
        self._lives_remaining = self._MAX_STARTING_LIVES
