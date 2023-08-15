namespace LinkedLists.Test;

public class P876Tests
{
    [Fact]
    public void Test1()
    {
        // Arrange
        int[] nums = { 1, 2, 3, 4, 5 };
        ListNode head = LinkedList.CreateFromArray(nums);
        int[] actual = nums[2..^0];
        // ListNode actual = LinkedList.CreateFromArray(nums[2..^0]);

        // Act
        ListNode resultList = P876.MiddleNode(head);
        int[] result = LinkedList.ToArray(resultList);

        // Assert
        Assert.Equal(actual, result);
    }

    [Fact]
    public void Test2()
    {
        // Arrange
        int[] nums = { 1, 2, 3, 4, 5, 6 };
        ListNode head = LinkedList.CreateFromArray(nums);
        int[] actual = nums[3..^0];
        // ListNode actual = LinkedList.CreateFromArray(nums[3..^0]);

        // Act
        ListNode resultList = P876.MiddleNode(head);
        int[] result = LinkedList.ToArray(resultList);

        // Assert
        Assert.Equal(actual, result);
    }
}