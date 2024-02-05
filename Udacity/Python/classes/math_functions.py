from collections.abc import Iterable
from typing import SupportsFloat, SupportsInt, Union

class MathFunctions:
    """Class containing math functions"""
    def __init__(self):
        pass

    _SupportsFloatOrIndex = Union[SupportsFloat, SupportsInt]

    def add(self, num1: _SupportsFloatOrIndex, num2: _SupportsFloatOrIndex) -> Union[float, int]:
        """
        Returns the sum of the two numbers
        
        Parameters
        ----------
        num1 : float | int
            First number
        num2 : float | int
            Second number
            
        Returns
        -------
        sum : float | int
            Sum of the two numbers
        """
        return num1 + num2

    def subtract(self,
                 num1: _SupportsFloatOrIndex,
                 num2: _SupportsFloatOrIndex) -> Union[float, int]:
        """
        Returns the difference of the two numbers
        
        Parameters
        ----------
        num1 : float | int
            First number
        num2 : float | int
            Second number
            
        Returns
        -------
        sum : float | int
            Difference of the two numbers
        """
        return num1 - num2

    def multiply(self,
                 num1: _SupportsFloatOrIndex,
                 num2: _SupportsFloatOrIndex) -> Union[float, int]:
        """
        Returns the product of the two numbers
        
        Parameters
        ----------
        num1 : float | int
            First number
        num2 : float | int
            Second number
            
        Returns
        -------
        sum : float | int
            Product of the two numbers
        """
        return num1 * num2

    def divide(self, num1: _SupportsFloatOrIndex, num2: _SupportsFloatOrIndex) -> Union[float, int]:
        """
        Returns the quotient of the two numbers
        
        Parameters
        ----------
        num1 : float | int
            First number
        num2 : float | int
            Second number
            
        Returns
        -------
        sum : float | int
            Quotient of the two numbers
            
        Raises
        ------
        ZeroDivisionError
            If the second number is 0
        """
        if num2 == 0:
            raise ZeroDivisionError("Cannot divide by 0")

        return num1 / num2

    def mean(self, num_list: Iterable[_SupportsFloatOrIndex]) -> Union[float, int]:
        """
        Returns the mean of the given list of numbers
        
        Parameters
        ----------
        num_list : list
            List of numbers
            
        Returns
        -------
        mean : float | int
            Mean of the given list of numbers
        """
        assert len(num_list) != 0
        return sum(num_list) / len(num_list)

    def median(self, num_list: Iterable[_SupportsFloatOrIndex]) -> Union[float, int]:
        """
        Returns the median of the given list of numbers
        
        Parameters
        ----------
        num_list : list
            List of numbers
            
        Returns
        -------
        median : float | int
            Median of the given list of numbers
        """
        assert len(num_list) != 0

        num_list.sort()
        if len(num_list) % 2 == 0:
            return num_list[len(num_list)//2] + num_list[len(num_list)//2 - 1]/2

        return num_list[len(num_list)//2]
