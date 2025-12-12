"""Defines the hand class for the blackjack application."""

from pydantic import BaseModel, PrivateAttr


class Hand(BaseModel):
    """Represents a player's hand during a game of blackjack."""

    name: str = None
    hand: list[str] = None
    _contains_ace: bool = PrivateAttr(False)
    ace_high: bool = True

    def __init__(self, hand):
        """Initialize the hand class."""
        super().__init__()
        self.hand = hand

    def set_ace_as_low(self):
        """Set whether aces should count as 11 or 1."""
        self.ace_high = False

    def top_card(self):
        """Return the top card from a hand."""
        return self.hand[0]

    def contains_ace(self):
        """Return whether the hand has an ace."""
        # If previously found an ace, return True
        if self._contains_ace:
            return self._contains_ace

        for card in self.hand:
            rank = card[:-1]
            if rank == "A":
                self._contains_ace = True
                return True

        return False

    def get_score(self) -> int:
        """Get the score from the player's hand."""
        score = 0
        for card in self.hand:
            rank = card[:-1]  # remove suit
            if rank.isdigit():
                score += int(rank)
            elif rank != "A":
                score += 10
            else:
                if self.ace_high:
                    score += 11
                else:
                    score += 1

        return score
