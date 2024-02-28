namespace LinkedLists;

public class ListNode
{
    public int val;
    public ListNode? next;
    
    public ListNode(int val, ListNode? next=null)
    {
        this.val = val;
        this.next = next;
    }
}

public static class LinkedList
{
    public static ListNode Insert(ListNode? head, int val)
    {
        if (head == null) {
            head = new(val);
        }
        else
        {
            ListNode ptr = head;
            while (ptr.next != null) {
                ptr = ptr.next;
            }
            ptr.next = new(val);
        }

        return head;
    }

    public static ListNode CreateFromArray(int[] nums)
    {
        ListNode? head = null;
        foreach (int num in nums)
        {
            head = Insert(head, num);
        }
        return head!;
    }

    public static int[] ToArray(ListNode? head)
    {
        List<int> list = new();
        while (head != null)
        {
            list.Add(head.val);
            head = head.next;
        }

        return list.ToArray();
    }

    public static void Display(ListNode? head)
    {
        while (head != null)
        {
            Console.Write(head.val.ToString() + " ");
            head = head.next;
        }
    }
}