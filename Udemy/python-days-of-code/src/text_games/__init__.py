"""Import games namespace."""

from .blackjack.blackjack import Blackjack
from .hangman.hangman import Hangman
from .higher_lower.higher_lower import HigherLower
from .number_guessing.number_guessing import NumberGuessing
from .quiz.quiz import Quiz
from .rock_paper_scissors.rock_paper_scissors import RockPaperScissors

__all__ = [
    "blackjack.blackjack",
    "hangman.hangman",
    "higher_lower.higher_lower",
    "number_guessing.number_guessing",
    "rock_paper_scissors.rock_paper_scissors",
    "quiz.quiz",
]
