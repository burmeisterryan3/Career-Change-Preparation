namespace Arrays;

// https://leetcode.com/problems/max-consecutive-ones/
public static class P485
{
    /* Constraints
     * 1 <= nums.length <= 10^5
     * nums[i] is either 0 or 1
     */
    public static int FindMaxConsecutiveOnes(int[] nums)
    {
        int max = 0;
        int current = 0;
        foreach (int num in nums)
        {
            if (num == 1)
            {
                current++;
                if (current > max)
                {
                    max = current;
                }
            } else
            {
                current = 0;
            }
        }

        return max;
    }
    // time complexity = O(n)
    // space complexity = O(1)
}