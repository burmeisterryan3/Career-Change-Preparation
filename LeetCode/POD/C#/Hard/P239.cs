namespace Hard;

public static class P239
{
    /* Constraints
     * 1 <= nums.length <= 10^5
     * -10^4 <= nums[i] <= 10^4
     * 1 <= k <= nums.length
     */
    public int[] MaxSlidingWindow(int[] nums, int k)
    {
        int numWindows = nums.Length - k + 1;
        int[] maxes = new int[numWindows];

        Queue<int> slidingWindow = new(k);
        SortedSet sortedWindowValues;

        for (int i = 0; i < k; i++)
        {
            int currentNum = nums[i];

            slidingWindow.Enqueue(currentNum);
            sortedWindowValues.Add(currentNum);
        }

        maxes[0] = sortedWindowValues.Max;
        for (int i = 1; i < numWindows; i++)
        {
            int oldBeginning = slidingWindow.Dequeue(i-1);
            
            int nextNum = nums[i+k-1];
            slidingWindow.Enqueue(nextNum);
            
            if (oldBeginning == maxes[i-1])
            {
                sortedSet.Remove(oldBeginning);
            }

        }
    }
}