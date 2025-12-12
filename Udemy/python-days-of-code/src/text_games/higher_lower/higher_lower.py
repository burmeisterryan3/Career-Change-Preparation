"""Day 13. Play the higher-lower game."""

from os import system
from random import randint
from typing import Literal

from game import DifficultyEnum, Game, ResultEnum
from pydantic import PrivateAttr

from .data import data
from .logo import logo, vs


class HigherLower(Game):
    """Defines the implementation of HigherLower."""

    def __init__(self):  # noqa: D107
        super().__init__()
        self._ties_possible = False
        self._NUM_PERSONALITIES: int = PrivateAttr(len(data))
        self._prior_personalities: list[int] = PrivateAttr([])
        self._score: int = PrivateAttr(0)
        self._prev_personality: dict[str, str] = PrivateAttr
        self._guesses_to_win: int = PrivateAttr(0)

    def _print_logo(self) -> None:
        system("clear")
        print(f"{logo}\n\n")

    def _print_welcome(self) -> None:
        self._print_logo()
        print("Welcome to Higher-Lower, the ultimate trivia game!")

    def _print_help(self) -> None:
        print()
        print(
            "Given two personalities, select the one you think is more popular based on the number of followers they have."
        )
        print()

    def start_playing(self) -> None:
        """Start the game with a welcome."""
        self._print_welcome()

        if self.difficulty == DifficultyEnum.easy:
            self._guesses_to_win = 5
        else:
            self._guesses_to_win = 10
        print(
            f"You need to guess {self._guesses_to_win} correctly in a row to win! Good luck!\n"
        )

        self._prev_personality = self._get_personality()

    def _get_personality(self) -> dict[str, str]:
        index = randint(0, self._NUM_PERSONALITIES - 1)
        while index in self._prior_personalities:
            index = randint(0, self._NUM_PERSONALITIES - 1)

        self._prior_personalities.append(index)
        return data[index]

    def _print_personalities(self, p2: dict[str, str]) -> None:
        print(
            f"Personality A: {self._prev_personality['name']}, a {self._prev_personality['description']}, from {self._prev_personality['country']}."
        )
        print(vs)
        print(
            f"Personality B: {p2['name']}, a {p2['description']}, from {p2['country']}."
        )

    def _get_user_pick(self) -> Literal["A", "B"]:
        pick = ""
        while pick not in ["A", "B"]:
            pick = input(
                "Which personality has more follower? Enter 'A' or 'B': "
            )

        return pick

    def _is_correct_pick(
        self, pick: Literal["A", "B"], p1_count: int, p2_count: int
    ) -> bool:
        if (pick == "A" and p1_count >= p2_count) or (
            pick == "B" and p2_count > p1_count
        ):
            return True
        else:
            return False

    def _user_turn(self) -> None:
        """Take a turn."""
        if self._prev_personality is None:
            self._prev_personality = self._get_personality()
        p2 = self._get_personality()

        self._print_personalities(p2)
        pick = self._get_user_pick()

        self._print_logo()
        if self._is_correct_pick(
            pick,
            self._prev_personality["follower_count"],
            p2["follower_count"],
        ):
            if pick == "B":
                self._prev_personality = p2
            self._score += 1

            print(f"You're right! Current score: {self._score}.")
            if self._score == self._guesses_to_win:
                self._result = ResultEnum.win
        else:
            self._result = ResultEnum.loss

    def _computer_turn(self) -> None:
        """No computer actions. Pass."""
        pass

    def output_result(self) -> None:
        """Print the final message."""
        if self._score == self._guesses_to_win:
            print(f"You scored {self._score} in a row. You won!")
        else:
            print(f"Sorry, that's wrong. Final score: {self._score}.")

    def reset(self) -> None:
        """Reset the values for a new game."""
        super().reset()
        self._score = 0
        self._prior_personalities = []
        self._prev_personality = None
