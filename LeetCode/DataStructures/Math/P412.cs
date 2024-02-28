namespace Math;

// https://leetcode.com/problems/fizz-buzz/
public static class P412
{
    public static IList<string> FizzBuzz(int n)
    {
        /* Constraints
         * 1 <= n <= 104
         */
        List<string> list = new();
        for (int i=1; i<=n; i++)
        {
            string result = "";

            if (i % 3 == 0)
            {
                result += "Fizz";
            }
            if (i % 5 == 0)
            {
                result += "Buzz";
            }

            if (string.IsNullOrEmpty(result))
            {
                result += i.ToString();
            }

            list.Add(result);
        }

        return list;
    }
    // time complexity = O(n)
    // space complexity = O(1)
}