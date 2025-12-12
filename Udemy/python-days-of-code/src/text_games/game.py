"""Define an abstract game class."""

from abc import ABC, abstractmethod
from enum import IntEnum
from time import sleep
from typing import final

from pydantic import BaseModel


class ResultEnum(IntEnum):
    """Enum for game result options."""

    incomplete = 0
    finished = 1
    win = 2
    loss = 3
    tie = 4


class DifficultyEnum(IntEnum):
    """Enum for difficulty level options."""

    easy = 1
    medium = 2
    hard = 3


class Game(ABC, BaseModel):
    """Define an abstract class that new games can inherit from."""

    def __init__(self):  # noqa: D107
        super().__init__()
        self._difficulty: DifficultyEnum = None
        self._continue_playing: bool = True
        self._result: ResultEnum = ResultEnum.incomplete
        self._total_wins: int = 0
        self._total_losses: int = 0
        self._total_ties: int = 0
        self._ties_possible: bool = True

    @abstractmethod
    def _print_logo(self) -> None:
        pass

    @abstractmethod
    def _print_help(self) -> None:
        pass

    @abstractmethod
    def _print_welcome(self) -> None:
        pass

    @property
    def result(self):
        """Return whether the game is over."""
        return self._result

    @property
    def difficulty(self) -> str:
        """Get the difficulty level for the game."""
        return self._difficulty

    @property
    def continue_playing(self) -> bool:
        """Return whether the player wants to play again."""
        return self._continue_playing

    @final
    def set_difficulty(self) -> None:
        """Set the difficulty level for a game."""
        difficulty = input("Choose a difficulty. Type 'easy' or 'hard': ")
        while difficulty not in ["easy", "hard"]:
            self._difficulty = input(
                "Invalid input! Choose a difficulty. Type 'easy' or 'hard': "
            )

        if difficulty == "easy":
            self._difficulty = DifficultyEnum.easy
        else:
            self._difficulty = DifficultyEnum.hard

    @abstractmethod
    def _print_help(self) -> None:
        pass

    @final
    def start_or_help(self) -> None:
        """Ask the user to start or for help before beginning."""
        start = ""
        while start != "s":
            start = input(
                "Type 's' to start or 'h' for help and a quick rules discussion: "
            )
            if start == "h":
                self._print_help()
                sleep(3)
                start = "s"

    @final
    def setup_game(self):
        """Set up the start to the game."""
        self._print_welcome()
        self.start_or_help()
        if self.difficulty is None:
            self.set_difficulty()

    @abstractmethod
    def start_playing(self):
        """Initialize your game."""
        pass

    @final
    def play_round(self):
        """Define what constitutes a turn in your game."""
        self._user_turn()
        self._computer_turn()

    @abstractmethod
    def _user_turn(self):
        """Define the user's turn."""
        pass

    @abstractmethod
    def _computer_turn(self):
        """Define the computer's turn."""
        pass

    @abstractmethod
    def output_result(self) -> None:
        """Print the final result of your game."""
        pass

    @final
    def ask_play_again(self) -> None:
        """Ask the user if they want to play again."""
        continue_playing = input("Play again? Type 'yes' or 'no'. ")
        while continue_playing not in ["yes", "no"]:
            continue_playing = input(
                "Invalid input! Play again? Type 'yes' or 'no'. "
            )

        if continue_playing == "yes":
            self._continue_playing = True
        else:
            self._continue_playing = False

    @abstractmethod
    def reset(self) -> None:
        """Reset any protected or private variables for a new game."""
        self._result = ResultEnum.incomplete

    @final
    def update_win_loss_tally(self) -> None:
        """Tally wins and losses."""
        if self._result == ResultEnum.win:
            self._total_wins += 1
        elif self._result == ResultEnum.loss:
            self._total_losses += 1
        elif self._ties_possible:
            self._total_ties += 1

    @final
    def output_final_tally(self) -> None:
        """Output the total win/loss tally."""
        print()
        print("Final Results:")
        print(
            f"   Total games: {self._total_losses + self._total_wins + self._total_ties}"
        )
        print(f"   Wins: {self._total_wins}")
        print(f"   Losses: {self._total_losses}")

        if self._ties_possible:
            print(f"   Ties: {self._total_ties}")
