using System.Diagnostics.CodeAnalysis;

namespace Arrays2D;

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
        // for(int m = 0; m < accounts.Length; m++)
        foreach (int[] customers in accounts)
        {
            int individualSum = 0;
            // for (int n = 0; n < accounts[m].Length; n++)
            foreach (int bank in customers)
            {
                // individualSum += accounts[m][n];
                individualSum += bank;
            }

            if (individualSum > maxSum)
            {
                maxSum = individualSum;
            }
        }

        return maxSum;
    }
}