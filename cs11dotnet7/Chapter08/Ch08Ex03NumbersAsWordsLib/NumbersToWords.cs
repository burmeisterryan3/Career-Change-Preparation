using System.Globalization;
using System.Numerics; // BigInteger

namespace NumbersToWordsLib
{
    public static class NumbersToWords
    {
        private static string[] smallNumbers = new string[]
        {
            "zero", "one", "two", "three", "four", "five", "six",
            "seven", "eight", "nine", "ten", "eleven", "twelve", "thirteen",
            "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"
        };

        private static string[] tens = new string[]
        {
            "", "", "twenty", "thirty", "forty", "fifty", "sixty",
            "seventy", "eighty", "ninety"
        };

        private static string[] scaleNumbers = new string[]
        {
            "", "thousand", "million", "billion", "trillion",
            "quadrillion", "quintillion"
        };

        private static int groups = 7; // numbers up to the quintillions

        public static string ToWords(this int number)
        {
            return ToWords((BigInteger)number);
        }

        public static string ToWords(this long number)
        {
            return ToWords((BigInteger)number);
        }

        public static string ToWords(this BigInteger number)
        {
            if (number == 0) return "zero";

            int[] digitGroups = new int[groups];

            BigInteger positive = BigInteger.Abs(number);

            // Divide number into groups of three digits
            for (int i = 0; i < groups; i++)
            {
                digitGroups[i] = (int)(positive % 1000);
                positive /= 1000;
            }

            string[] textGroups = new string[groups];

            // Convert each group of three digits to text
            for (int i = 0; i < groups; i++)
            {
                if (digitGroups[i] != 0)
                {
                    textGroups[i] = ThreeDigitGroupToWords(digitGroups[i]);
                }
            }

            string combined = textGroups[0];
            bool commaNeeded = digitGroups[0] != 0;

            // Add three digit text groups together and add scale, e.g. thousand, million, billion, etc.,  to corresponding digits
            for (int i = 1; i < groups; i++)
            {
                if (digitGroups[i] != 0)
                {
                    string prefix = textGroups[i] + " " + scaleNumbers[i];
                    if (commaNeeded) prefix += ", ";

                    combined = prefix + combined;
                }
            }

            if (number < 0) combined = "negative " + combined;

            return combined;
        }

        private static string ThreeDigitGroupToWords(int threeDigits)
        {
            string groupText = "";

            int hundreds = threeDigits / 100;
            int tensUnits = threeDigits % 100;
            int tens = tensUnits / 10;
            int units = tensUnits % 10;

            if (hundreds != 0)
            {
                groupText += smallNumbers[hundreds] + " hundred";
                if (tensUnits != 0) groupText += " ";
            }

            if (tens >= 2)
            {
                groupText += NumbersToWords.tens[tens];
                if (units != 0)
                {
                    groupText += "-" + smallNumbers[units];
                }
            }
            else if (tensUnits != 0)
            {
                groupText += smallNumbers[tensUnits];
            }

            return groupText;
        }
    }
}