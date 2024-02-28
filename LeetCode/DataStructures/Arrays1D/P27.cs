namespace Arrays;

// https://leetcode.com/problems/remove-element/
public static class P27
{
    /* Constraints
     * 0 <= nums.length <= 100
     * 0 <= nums[i] <= 50
     * 0 <= val <= 100
     */
    public static int RemoveElement(int[] nums, int val)
    {
        int count = 0;
        for (int i=0; i < nums.Length; i++)
        {
            if (nums[i] == val)
            {
                count++;
            }
            else
            {
                nums[i-count] = nums[i];
            }
        }
        return nums.Length-count;
    }
    // time complexity = O(n)
    // space complexity = O(1)
}