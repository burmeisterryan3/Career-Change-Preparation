partial class Program
{
    /// <summary>
    /// Output the times tables for number from 1 to size.
    /// </summary>
    /// <param name="number"></param>
    /// <param name="size"></param>
    static void TimesTable(byte number, byte size = 12)
    {
        WriteLine($"This is the {number} times table with {size} rows:");
        for (int row = 1; row <= size; row++)
        {
            WriteLine($"{row} x {number} = {row * number}");
        }
        WriteLine();
    }

    /// <summary>
    /// Calculate the tax for the given amount and associated region.
    /// </summary>
    /// <param name="amount"></param>
    /// <param name="twoLetterRegionCode"></param>
    /// <returns>Tax value</returns>
    static decimal CalculateTax(decimal amount, string twoLetterRegionCode)
    {
        decimal rate;
        rate = twoLetterRegionCode switch
        {
            "CH" => 0.08M, // Switzerland
            "DK" or "NO" => 0.25M, // Denmark or Norway
            "GB" or "FR" => 0.2M, // United Kingdom or France
            "HU" => 0.27M, // Hungary
            "OR" or "AK" or "MT" => 0.0M, // Oregon, Alaska, or Montana
            "ND" or "WI" or "ME" or "VA" => 0.05M, // North Dakota, Wisconsin, Maine, or Virginia
            "CA" => 0.0825M, // California
            _ => 0.06M // most US states
        };
        return amount * rate;
    }

    /// <summary>
    /// Pass a 32-bit integer and it will be converted onto its ordinal equivalent.
    /// </summary>
    /// <param name="number">Number as a cardinal value e.g. 1, 2, 3, and so on.</param>
    /// <returns>Number as an ordinal value e.g. 1st, 2nd, 3rd, and so on.</returns>
    static string CardinalToOrdinal(int number)
    {
        int lastTwoDigits = number % 100;

        switch(lastTwoDigits)
        {
            case 11:
            case 12:
            case 13:
                return $"{number:N0}th";
            default:
                int lastDigit = number % 10;
                string suffix = lastDigit switch
                {
                    1 => "st",
                    2 => "nd",
                    3 => "rd",
                    _ => "th"
                };
                return $"{number:N0}{suffix}";
        };
    }

    /// <summary>
    /// Runs the CardinalToOrdinal function from 1 to 150.
    /// </summary>
    static void RunCardinalToOrdinal()
    {
        for (int i = 1; i <= 150; i++)
        {
            Write($"{CardinalToOrdinal(i)} ");
        }
        WriteLine();
    }

    /// <summary>
    /// Compute the factorial of a 32-bit integer
    /// </summary>
    /// <param name="number"></param>
    /// <returns></returns>
    /// <exception cref="ArgumentException"></exception>
    static int Factorial(int number)
    {
        if (number < 0)
        {
            throw new ArgumentException(
                message: "The factorial function is defined for " +
                         $"non-negative integers only. Input: { number }", 
                paramName: nameof(number));
        }
        else if (number == 0)
        {
            return 1;
        }
        else
        {
            checked // for overflow, int overflows for numbers >= 13
            {
                return number * Factorial(number - 1);
            }
        }
    }
    
    /// <summary>
    /// Runs the Factorial function from -2 to 15.
    /// </summary>
    static void RunFactorial()
    {
        for (int i = -2; i <= 15; i++)
        {
            try
            {
                WriteLine($"{i}! = {Factorial(i):N0}");
            }
            catch (OverflowException)
            {
                WriteLine($"{i}! is to big for a 32-bit integer.");
            }
            catch (Exception e)
            {
                WriteLine($"{i}! throws {e.GetType()}: {e.Message}");
            }
        }
    }

    /// <summary>
    /// Compute the nth Fibonacci number using iterative programming
    /// </summary>
    /// <param name="term"></param>
    /// <returns>nth Fibonacci number</returns>
    static int FibImperative(int term)
    {
        if (term == 1)
        {
            return 0;
        }
        else if (term == 2)
        {
            return 1;
        }
        else
        {
            return FibImperative(term - 1) + FibImperative(term - 2);
        }
    }

    /// <summary>
    /// Runs the FibImperative function from 1 to 30.
    /// </summary>
    static void RunFibImperative()
    {
        for (int i = 1; i <= 30; i++)
        {
            WriteLine("The {0} term of the Fibonacci sequence is {1:N0}.",
            arg0: CardinalToOrdinal(i),
            arg1: FibImperative(term: i));
        }
    }

    /// <summary>
    /// Compute the nth Fibonnaci number using functional programming
    /// </summary>
    /// <param name="term"></param>
    /// <returns>nth Fibonacci number</returns>
    static int FibFunctional(int term) =>
        term switch
        {
            1 => 0,
            2 => 1,
            _ => FibFunctional(term - 1) + FibFunctional(term - 2)
        };

    /// <summary>
    /// Runs the FibFunctional function from 1 to 30.
    /// </summary>
    static void RunFibFunctional()
    {
        for (int i = 1; i <= 30; i++)
        {
            WriteLine("The {0} term of the Fibonacci sequence is {1:N0}.",
            arg0: CardinalToOrdinal(i),
            arg1: FibFunctional(term: i));
        }
    }

}