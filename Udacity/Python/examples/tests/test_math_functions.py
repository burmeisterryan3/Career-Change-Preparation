"""Tests the math functions"""
import unittest
from classes.math_functions import MathFunctions

class TestMathFunctions(unittest.TestCase):
    """Tests the math functions"""""
    def setUp(self):
        self.math_functions = MathFunctions()

    def test_addition(self):
        """Tests the addition function"""
        self.assertEqual(self.math_functions.add(2, 3), 5)

    def test_subtraction(self):
        """Tests the subtraction function"""
        self.assertEqual(self.math_functions.subtract(3, 2), 1)

    def test_multiplication(self):
        """Tests the multiplication function"""
        self.assertEqual(self.math_functions.multiply(2, 3), 6)

    def test_division(self):
        """Tests the division function"""
        self.assertEqual(self.math_functions.divide(6, 3), 2)

    def test_division_by_zero(self):
        """Tests the division function with a zero denominator"""
        with self.assertRaises(ZeroDivisionError):
            self.math_functions.divide(6, 0)
            
if __name__ == '__main__':
    unittest.main()
    