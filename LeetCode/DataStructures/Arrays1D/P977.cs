namespace Arrays;

// https://leetcode.com/problems/squares-of-a-sorted-array/
public static class P977
{
    /* Constraints
     * 1 <= nums.length <= 104
     * -104 <= nums[i] <= 104
     * nums is sorted in non-decreasing order.
     */
   public static int[] SortedSquares(int[] nums)
    {
        int length = nums.Length;
        int[] squares = new int[length];

        int left = 0;
        int right = length-1;

        for (int i=right; i>=0; i--)
        {
            if (Math.Abs(nums[right]) > Math.Abs(nums[left]))
            {
                squares[i] = nums[right];
                right--;
            }
            else
            {
                squares[i] = nums[left];
                left++;
            }

            squares[i] *= squares[i];
        }

        return squares;
    }
    // time complexity = O(n)
    // space complexity = O(n)
}