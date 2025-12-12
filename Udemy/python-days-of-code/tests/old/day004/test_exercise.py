from pydantic import ValidationError
import day004.src.exercises as e
import pytest

def test_coin_flips():
    n_flips = 10000
    unbiased = e.coin_flips(n_flips=n_flips)["heads"] / n_flips
    assert unbiased > 0.45 and unbiased < 0.55

    biased = e.coin_flips(n_flips=n_flips, bias=0.8)["heads"] / n_flips
    assert biased > 0.75 and biased < 0.85

def test_random_buyer():
    names = ["Michael", "Ben", "Susie", "Jen"]
    assert e.random_buyer(names) in names
    
    with pytest.raises(ValidationError):
        e.random_buyer([])

def test_treasure_hider():
    loc = "B2"
    assert e.treasure_hider(loc)[1][1] == "X"