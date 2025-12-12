"""Day 11. Blackjack class."""

from os import system

from game import DifficultyEnum, Game, ResultEnum
from pydantic import PrivateAttr

from .deck import Deck
from .hand import Hand
from .logo import logo


class Blackjack(Game):
    """Defines the blackjack class."""

    def __init__(self):  # noqa: D107
        super().__init__()
        self._dealer_hand: Hand = PrivateAttr
        self._player_hand: Hand = PrivateAttr
        self._deck: Deck = PrivateAttr

    def _print_logo(self) -> None:
        system("clear")
        print(f"{logo}\n\n")

    def _print_welcome(self) -> None:
        """Print welcome message for user."""
        self._print_logo()
        print("Welcome to Blackjack, the ultimate game of 21!")

    def _print_help(self) -> None:
        print()
        print("Use your hand to try and score better than the dealer.")
        print("Ace = 1 or 11, Numerical Cards = their #, Face Cards = 10")
        print("Dealer wins if they score 21 or have a higher score than you.")
        print(
            "You win if you have a higher score than the dealer. A tie is a 'push'."
        )
        print(
            "Dealer must hit when they have < 17 points. Aces are always 11 for a dealer."
        )
        print()

    def _print_hand_and_score(self) -> None:
        print(
            f"Your cards: [{', '.join(self._player_hand.hand)}], current score: {self._player_hand.get_score()}"
        )

    def start_playing(self) -> None:
        """Start and configure the game."""
        self._print_welcome()

        if self.difficulty == DifficultyEnum.easy:
            num_decks = 1
        else:
            num_decks = 3

        self._deck = Deck(num_decks)
        self._dealer_hand, self._player_hand = self._deck.deal_hands()

        # With double aces, the user would bust without counting them as 1
        if self._player_hand.get_score() == 22:
            self._player_hand.ace_high = False

        self._print_hand_and_score()
        print(f"Dealer's top card: {self._dealer_hand.top_card()}")

        if self._player_hand.get_score() == 21:
            self._result = ResultEnum.finished
            self._computer_turn()
        elif (
            self._player_hand.get_score() != 21
            and self._player_hand.contains_ace()
        ):
            self._ask_to_change_ace()

    def _ask_to_change_ace(self) -> None:
        change_ace = ""
        while change_ace not in ["y", "n"]:
            if self._player_hand.ace_high:
                change_ace = input(
                    "\nYou have an 'A' worth 11. Would you like to make it worth 1? 'y' or 'n'? "
                )
            else:
                change_ace = input(
                    "\nYou have an 'A' worth 1. Would you like to make it worth 11? 'y' or 'n'? "
                )

        if change_ace == "y":
            self._player_hand.ace_high = not self._player_hand.ace_high

    def _wants_to_hit(self) -> bool:
        hit = input("\nType 'y' to get another card. Type 'n' to pass: ")
        while hit not in ["y", "n"]:
            hit = input(
                "Invalid input! Type 'y' to get another card. Type 'n' to pass: "
            )

        if hit == "y":
            return True
        else:
            return False

    def _hit(self, dealer=False) -> None:
        """Take an additional card."""
        next_card = self._deck.deal_card()

        if dealer:
            print(f"\nDealer's next card is: {next_card}.")
            self._dealer_hand.hand.append(next_card)
        else:
            print(f"\nPlayer's next card is: {next_card}.")
            self._player_hand.hand.append(next_card)
            if self._player_hand.contains_ace():
                self._ask_to_change_ace()
            self._print_hand_and_score()

    def _user_turn(self) -> None:
        """Play the user's hand."""
        if self._wants_to_hit():
            self._hit()
            if self._player_hand.get_score() >= 21:
                self._result = ResultEnum.finished
        else:
            self._result = ResultEnum.finished

    def _computer_turn(self) -> None:
        """Play the dealer's hand."""
        if (
            self._result == ResultEnum.finished
            and self._player_hand.get_score() <= 21
        ):
            score = self._dealer_hand.get_score()
            while score < 17:
                self._hit(dealer=True)
                score = self._dealer_hand.get_score()

    def output_result(self) -> None:
        """Print the final result."""
        player_final_score = self._player_hand.get_score()
        dealer_final_score = self._dealer_hand.get_score()

        print(
            f"\nYour final hand: [{', '.join(self._player_hand.hand)}], final score: {player_final_score}"
        )
        print(
            f"Dealer's final hand: [{', '.join(self._dealer_hand.hand)}], final score: {dealer_final_score}"
        )

        if player_final_score > 21:
            print("\nYou went over 21. You lose!")
            self._result = ResultEnum.loss
        elif dealer_final_score > 21:
            print("\nDealer went over 21. You win!")
            self._result = ResultEnum.win
        elif dealer_final_score == 21:
            print("\nDealer scored 21. You lose!")
            self._result = ResultEnum.loss
        elif player_final_score > dealer_final_score:
            print("\nYou have a better hand. You win!")
            self._result = ResultEnum.win
        elif player_final_score < dealer_final_score:
            print("\nDealer has a better hand. You lose!")
            self._result = ResultEnum.loss
        else:
            print("\nPush! You tied the dealer!")
            self._result = ResultEnum.tie

    def reset(self) -> None:
        """Reset the values for a new game."""
        super().reset()
        self._dealer_hand = None
        self._player_hand = None
        self._deck = None
