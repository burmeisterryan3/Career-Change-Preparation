namespace Arrays;

// https://leetcode.com/problems/merge-sorted-array/
public static class P88
{
    /* Constraints
     * nums1.length == m + n
     * nums2.length == n
     * 0 <= m, n <= 200
     * 1 <= m + n <= 200
     * -109 <= nums1[i], nums2[j] <= 109
     */
    public static void Merge(int[] nums1, int m, int[] nums2, int n)
    {
        int last1 = m-1;
        int last2 = n-1;

        for (int i=m+n-1; last2>=0; i--)
        {
            if (last1 < 0 || nums2[last2] > nums1[last1] )
            {
                nums1[i] = nums2[last2];
                last2--;
            }
            else // nums1[last1] > nums2[last2]
            {
                nums1[i] = nums1[last1];
                last1--;
            }
        }
    }
    // time complexity = O(m+n)
    // space complexity = O(1)
}