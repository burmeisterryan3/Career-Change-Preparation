"""Tests for the blackjack application."""

from random import randint

from deck import Deck
from pytest import fixture
from scipy import stats


# Arrange
@fixture
def deck():
    """Set a deck for tests' use."""
    return Deck(shuffle=False)


@fixture
def large_deck():
    """Set a large deck for tests' use."""
    return Deck(shuffle=False, num_decks=3)


def test_deal_card_top_card(deck, large_deck):
    """Test dealing top card."""
    assert deck.deal_card() == "KS"
    assert large_deck.deal_card() == "KS"


def test_deal_card_middle_card(deck, large_deck):
    """Test dealing middle card."""
    # Act
    for _ in range(12):
        deck.deal_card()
        large_deck.deal_card()

    # Assert
    assert deck.deal_card() == "10S"
    assert large_deck.deal_card() == "QS"


def test_shuffle():
    """Ensure the shuffle and deal functionality distributes cards uniformly."""
    random_draws = []
    for _ in range(10000):
        d = Deck()
        random_draws += [
            d.convert_rank_to_number(d.deal_card(), ace_high=False)
        ]

    uniform_draws = []
    for _ in range(10000):
        uniform_draws.append(randint(1, 13))

    assert stats.kstest(random_draws, uniform_draws).pvalue > 0.05


def test_deal_hands(deck):
    """Test dealing hands to multiple players."""
    hands = deck.deal_hands()
    assert len(hands) == 2
    assert len(hands[0].hand) == len(hands[1].hand) == 2
