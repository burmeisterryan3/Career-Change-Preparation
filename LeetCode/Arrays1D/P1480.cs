namespace Arrays;

public static class P1480
{
    /* Constraints
     * 1 <= nums.length <= 1000
     * -10^6 <= nums[i] <= 10^6
     */
    public static int[] RunningSum1dArray(int[] nums)
    {
        for (int i = 1; i < nums.Length; i++)
        {
            nums[i] += nums[i - 1];
        }
        return nums;
    }
}
