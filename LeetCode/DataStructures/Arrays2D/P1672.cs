namespace Arrays2D;

// https://leetcode.com/problems/richest-customer-wealth/
public static class P1672
{
    /* Constraints
     * m == accounts.length
     * n == accounts[i].length
     * 1 <= m, n <= 50
     * 1 <= accounts[i][j] <= 100
     */
    public static int MaximumWealth(int[][] accounts)
    {
        int maxSum = 0;
        foreach (int[] customers in accounts) // m
        {
            int individualSum = 0;
            foreach (int bank in customers) // n
            {
                individualSum += bank;
            }

            if (individualSum > maxSum)
            {
                maxSum = individualSum;
            }
        }

        return maxSum;
    }
    // time complexity = O(nm)
    // space complexity = O(1)
}