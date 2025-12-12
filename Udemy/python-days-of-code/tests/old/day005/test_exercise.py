import day005.src.exercises as e
import pytest
from pydantic import ValidationError

def test_height_metrics():
    assert e.height_metrics([151, 145, 179]) == (475, 3, 158)
    assert e.height_metrics([156, 178, 165, 171, 187]) == (857, 5, 171)
    assert e.height_metrics([180, 124, 165, 173, 189, 169, 146]) == (1146, 7, 164)

def test_high_score():
    assert e.high_score([78, 65, 89, 86, 55, 91, 64, 89]) == 91
    assert e.high_score([150, 142, 185, 120, 171, 184, 149, 199]) == 199
    assert e.high_score([24, 59, 68]) == 68

def test_sum_even():
    assert e.sum_even(10) == 30
    assert e.sum_even(52) == 702
    with pytest.raises(ValidationError):
        e.sum_even(1001)
        e.sum_even(-1)