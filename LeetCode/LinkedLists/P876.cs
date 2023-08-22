namespace LinkedLists;

// https://leetcode.com/problems/middle-of-the-linked-list/
public static class P876
{
    public static ListNode MiddleNode(ListNode head)
    {
        /* Constraints
        * The number of nodes in the list is in the range [1, 100].
        * 1 <= Node.val <= 100
        */
        ListNode? iter = head;
        ListNode middle = head!;

        while (iter != null && iter.next != null)
        {
            iter = iter.next.next;
            middle = middle.next!;
        }

        return middle;
    }
    // time compexity = O(m)
    // space complexity = O(1)
}
