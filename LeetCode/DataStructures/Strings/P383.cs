namespace Strings;

// https://leetcode.com/problems/ransom-note/
public static class P383
{
    /* Constraints
     * 1 <= ransomNote.length, magazine.length <= 10^5
     * ransomNote and magazine consist of lowercase English letters
     */
    public static bool CanConstruct(string ransomNote, string magazine) {
        Dictionary<char, int> charCounts = new(); // k = 26
        
        foreach (char c in magazine) // m
        {

            if (charCounts.ContainsKey(c))
            {
                charCounts[c] += 1;
            }
            else 
            {
                charCounts.Add(c, 1);
            }
        }

        foreach (char c in ransomNote) // bounded by m (ransomNote.Length <= magazine.Length)
        {
            if (charCounts.ContainsKey(c))
            {
                charCounts[c]--;
                if (charCounts[c] == 0)
                {
                    charCounts.Remove(c);
                }
            }
            else
            {
                return false;
            }
        }

        return true;
    }
    // time complexity = O(m)
    // space complexity = O(1) - dictionary size <= 26
}