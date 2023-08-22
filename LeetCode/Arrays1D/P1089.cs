namespace Arrays;

// https://leetcode.com/problems/duplicate-zeros/
public static class P1089
{
    /* Constraints
     * 1 <= arr.length <= 104
     * 0 <= arr[i] <= 9
     */
   public static void DuplicateZeros(int[] arr)
    {
        int duplicates = 0;
        int length = arr.Length-1;

        for(int i=0; i<=length-duplicates; i++)
        {
            if (arr[i] == 0)
            {
                if (i == length-duplicates)
                {
                    arr[length] = 0;
                    length--;
                    break;
                }
                duplicates++;
            }
        }

        for (int i=length-duplicates; i>=0 && duplicates!=0; i--)
        {
            if (arr[i] == 0)
            {
                arr[i+duplicates] = 0;
                duplicates--;
            }
            arr[i+duplicates] = arr[i];
        }
    }
    // time complexity = O(n)
    // space complexity = O(1)
}