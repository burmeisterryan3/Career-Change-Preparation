from pydantic import ValidationError
import day002.src.exercise as e
import math as m
import pytest

def test_add_digits():
    assert e.add_digits("123") == 6
    assert e.add_digits("25") == 7

def test_bmi_calculator():
    assert m.isclose(e.bmi_calculator(1.65, 72), 26.4)

def test_weeks_in_life():
    with pytest.raises(ValidationError):
        e.life_in_weeks(-1)

    assert e.life_in_weeks(53) == 1924
    assert e.life_in_weeks(12) == 4056
    assert e.life_in_weeks(90) == 0

def test_tip_calculator():
    with pytest.raises(ValidationError):
        e.tip_calculator(-1, 20)
        e.tip_calculator(20, -1)
        e.tip_calculator(20, 1, -1)
    
    assert m.isclose(e.tip_calculator(150, 12, 5), 33.6)