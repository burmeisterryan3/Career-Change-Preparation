"""Define the quiz game."""

import random
from os import system

from game import DifficultyEnum, Game, ResultEnum
from pydantic import NonNegativeInt

from .data import question_data
from .logo import logo
from .question import Question


class Quiz(Game):
    """Define the quiz class."""

    def __init__(self):  # noqa: D107
        super().__init__()
        self._question_bank = [
            Question(question["text"], question["answer"])
            for question in question_data
        ]
        self._question_number: NonNegativeInt = 0
        self._ties_possible = False

    def _print_logo(self) -> None:
        system("clear")
        print(f"{logo}\n\n")

    def _print_welcome(self) -> None:
        self._print_logo()
        print("Welcome to the Quiz Game!")

    def _print_help(self) -> None:
        print()
        print("Try to answer as many questions in a row as you can.")
        print("Easy - Win after 3 guesses in a row")
        print("Hard - Win after 5 guesses in a row")
        print()

    def _print_help(self) -> None:
        pass

    def start_playing(self):
        """Initialize the quiz game."""
        self._print_welcome()

        if self._difficulty == DifficultyEnum.easy:
            self._guesses_remaining = 3
        else:
            self._guesses_remaining = 5

        self._question_order = random.sample(
            self._question_bank, self._guesses_remaining
        )

    def _current_question(self):
        """Identify the current question."""
        return self._question_order[self._question_number]

    def _user_turn(self):
        """Define the user's turn."""
        question = self._current_question()

        guess = input(
            f"Q.{self._question_number + 1}: {question.text} (True/False)?: "
        )

        while guess not in ["True", "False"]:
            guess = input(
                f"Q.{self._question_number + 1}: {question.text} (True/False)?: "
            )

        if guess == question.answer:
            self._guesses_remaining -= 1
            self._question_number += 1
            if self._guesses_remaining == 0:
                self._result = ResultEnum.win
        else:
            self._result = ResultEnum.loss

    def _computer_turn(self):
        """Define the computer's turn."""
        pass

    def output_result(self) -> None:
        """Print the final result of your game."""
        if self._result == ResultEnum.win:
            print(
                f"Awesome job! You answered {self._question_number} in a row!"
            )
        else:
            print("Oh no! You answered the question incorrectly!")

    def reset(self) -> None:
        """Reset any protected or private variables for a new game."""
        super().reset()
        self._question_number = 0
