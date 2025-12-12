"""Defines the deck class used for the blackjack application."""

import logging
import random

from pydantic import BaseModel, PrivateAttr

from .hand import Hand

logger = logging.getLogger(__name__)


class Deck(BaseModel):
    """Deck class."""

    _RANKS: list[str] = PrivateAttr(
        [
            "A",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "10",
            "J",
            "Q",
            "K",
        ]
    )
    _SUITS: list[str] = PrivateAttr(["H", "D", "C", "S"])
    _deck: list[str] = PrivateAttr()

    def __init__(
        self,
        shuffle: bool = True,
        num_decks: int = 1,
    ):
        """Initialize the deck class.

        Note that we must call BaseModel's init prior to setting private
        attributes in our classes init, i.e., not the PrivateAttr
        constructor, given how pydantic sets private variables

        See the below links for more details
        https://github.com/pydantic/pydantic/issues/7855#issuecomment-1769315791
        https://stackoverflow.com/questions/74211366/pydantic-how-to-access-updated-values-for-privateattr
        """
        super().__init__()
        self._build_deck(num_decks)
        if shuffle:
            self.shuffle()

    def _build_deck(self, num_decks: int) -> None:
        self._deck = [
            card
            for rank in self._RANKS
            for suit in self._SUITS
            for card in [rank + suit] * num_decks
        ]

    def shuffle(self):
        """Shuffle the deck."""
        random.shuffle(self._deck)

    def deal_card(self) -> str:
        """Return the top card from the deck."""
        return self._deck.pop()

    def deal_hands(self, num_hands=2, hand_size=2) -> list[Hand]:
        """Return a list of cards representing a hand."""
        # [[]] * num_hands creates lists with the same memory location
        hands = [Hand([]) for _ in range(num_hands)]
        for i in range(num_hands * hand_size):
            hands[i % num_hands].hand.append(self.deal_card())
        return hands

    def convert_rank_to_number(self, card: str, ace_high: bool = True) -> int:
        """Convert rank of card, e.g., 'K', to numerical value, e.g., 13."""
        num_rank = self._RANKS.index(card[:-1]) + 1
        if ace_high and num_rank == 1:
            num_rank = 14
        return num_rank
