"""Test exercise from Day 8"""

from lessons.exercises import prime_checker  # type: ignore


def test_prime_checker():
    assert not prime_checker(0)
    assert not prime_checker(1)
    assert prime_checker(2)
    assert not prime_checker(8)
    assert not prime_checker(87)
    assert prime_checker(97)
