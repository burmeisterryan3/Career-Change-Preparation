namespace Ch04Ex02PrimeFactorsLib
{
    public class PrimeFactors
    {
        public string Factorize(int num)
        {
            List<int> factorsList = new();
            int divisor = 2;
            int remaining = num / 2;
            int currentNum = num;
            bool numIsNegative = false;

            // If num is negative, compute factors like positive
            // -1 will be added as factor at the end
            if (num < 0)
            {
                numIsNegative = true;
                // currentNum *= -1; // Find positive factors
                remaining *= -1;
            }

            while (divisor <= remaining)
            {
                if (num % divisor == 0)
                {
                    factorsList.Add(divisor);
                    currentNum /= divisor;
                    remaining = currentNum;
                }
                else
                {
                    divisor++;
                }
            }

            
            int[] factorsArray;
            if (!factorsList.Any()) // if factors is still empty, then num is prime
            {
                factorsList.Add(num);
                factorsArray = factorsList.ToArray();
            } else
            {
                // Convert to array and sort for printing
                factorsArray = factorsList.ToArray();
                Array.Sort(factorsArray);
                Array.Reverse(factorsArray);

                // Multiple by -1 if negative
                if (numIsNegative)
                {
                    factorsArray[factorsArray.GetUpperBound(0)] *= -1;
                }
            }

            return $"Prime factors of {num} are: {string.Join(" x ", factorsArray)}";
        }
    }
}