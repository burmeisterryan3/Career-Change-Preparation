namespace Arrays;

// https://leetcode.com/problems/remove-duplicates-from-sorted-array/
public static class P26
{
    /* Constraints
     * 1 <= nums.length <= 3 * 104
     * -100 <= nums[i] <= 100
     * nums is sorted in non-decreasing order
     */
    public static int RemoveDuplicates(int[] nums)
    {
        int j = 1;
        for (int i=1; i<nums.Length; i++)
        {
            if (nums[i] != nums[i-1])
            {
                nums[j] = nums[i];
                j++;
            }
        }
        return j;
    }
    // time complexity = O(N)
    // space complexity = O(1)
}