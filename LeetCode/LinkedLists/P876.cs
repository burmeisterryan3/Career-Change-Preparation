namespace LinkedLists;

public static class P876
{
    public static ListNode MiddleNode(ListNode head)
    {
        /* Constraints
        * The number of nodes in the list is in the range [1, 100].
        * 1 <= Node.val <= 100
        */
        int length = 0;
        ListNode? iter = head;
        ListNode? half = head;

        while (iter != null)
        {
            iter = iter.next;
            length++;

            if (length % 2 == 0)
            {
                half = half.next!;
            }
        }

        return half!;
    }
}
