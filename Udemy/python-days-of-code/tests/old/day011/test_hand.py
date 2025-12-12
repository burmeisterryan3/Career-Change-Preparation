"""Test the hand class."""

from deck import Deck
from hand import Hand
from pytest import fixture


@fixture
def deck():
    """Initialize deck fixture."""
    return Deck(shuffle=False)


@fixture
def hand_with_ace():
    """Initialize hand with an ace."""
    return Hand(["AS", "10H"])


@fixture
def hand_no_ace():
    """Initialize hand without an ace."""
    return Hand(["2C", "JS"])


def test_get_score_from_deck(deck):
    """Get score from a single hand without shuffling."""
    hand = Hand(deck.deal_hands(num_hands=1, hand_size=2)[0].hand)
    assert hand.get_score() == 20


def test_get_score_from_hands(hand_no_ace, hand_with_ace):
    """Test scores from multiple hands."""
    assert hand_with_ace.get_score() == 21
    assert hand_no_ace.get_score() == 12


def test_get_score_ace_low(hand_with_ace):
    """Test score after switching ace to low score."""
    hand_with_ace.set_ace_as_low()
    assert hand_with_ace.get_score() == 11
