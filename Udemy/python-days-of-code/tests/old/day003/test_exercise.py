import day003.src.exercises as e

def test_is_even():
    assert not e.is_even(3)
    assert e.is_even(4)
    assert e.is_even(0)
    assert not e.is_even(-3)

def test_bmi_characterization():
    assert e.bmi_characterization(1.80, 81) == "slightly overweight"
    assert e.bmi_characterization(1.75, 98) == "obese"
    assert e.bmi_characterization(1.50, 54) == "normal weight"
    assert e.bmi_characterization(1.75, 65) == "normal weight"

def test_is_leap_year():
    assert e.is_leap_year(2000)
    assert not e.is_leap_year(1993)
    assert not e.is_leap_year(2100)
    assert e.is_leap_year(1776)

def test_pizza_price():
    assert e.pizza_price("L", "Y", "N") == 28
    assert e.pizza_price("S", "N", "Y") == 16
    assert e.pizza_price("L", "N", "N") == 25
    assert e.pizza_price("M", "Y", "N") == 23
    assert e.pizza_price("L", "Y", "Y") == 29

def test_love_calculator():
    assert e.love_calculator("Angela Yu", "Jack Bauer") == 53
    assert e.love_calculator("Kayne West", "Kim Kardashian") == 42
    assert e.love_calculator("Brad Pitt", "Jennifer Anniston") == 73
    assert e.love_calculator("Prince William", "Kate Middleton") == 67