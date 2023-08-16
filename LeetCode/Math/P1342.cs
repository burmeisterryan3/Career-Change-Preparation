namespace Math;

public static class P1342
{
    public static int NumberOfSteps(int num)
    {
        /* Constraints
         * 0 <= num <= 10^6
         */
        int steps = 0;
        while (num != 0)
        {
            if (num % 2 == 0){
                num /= 2;
            } else 
            {
                num -= 1;
            }

            steps++;
        }

        return steps;
    }
    // time complexity = O(logn)
    // space complexity = O(1)
}