namespace Arrays;

// https://leetcode.com/problems/find-numbers-with-even-number-of-digits/
public static class P1295
{
    /* Constraints
     * 1 <= nums.length <= 500
     * 1 <= nums[i] <= 10^5
     */
    public static int FindNumbers(int[] nums)
    {
        short evenNums = 0; // max evenNums is 500
        for (int i=0; i<nums.Length; i++) // n
        {
            byte count = 0; // max length is 6
            while (nums[i] > 0 )
            {
                nums[i] /= 10;
                count++;
            }

            if (count % 2 == 0)
            {
                evenNums++;
            }
        }
        return evenNums;
    }
    // time complexity = O(n)
    // space complexity = O(1)
}