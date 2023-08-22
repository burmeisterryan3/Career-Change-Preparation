namespace Arrays.Test;

public class P27Tests
{
    [Fact]
    public void Test1()
    {
        // Arrange
        int[] nums = { 3, 2, 2, 3 };
        int val = 3;
        int[] expected = { 2, 2, 2, 3 };
        int expectedLength = 2;
        
        // Act
        int length = P27.RemoveElement(nums, val);
        
        // Assert
        Assert.Equal(expected, nums);
        Assert.Equal(expectedLength, length);
    }

    [Fact]
    public void Test2()
    {
        // Arrange
        int[] nums = { 0, 1, 2, 2, 3, 0, 4, 2 };
        int val = 2;
        int[] expected = { 0, 1, 3, 0, 4, 0, 4, 2 };
        int expectedLength = 5;
        
        // Act
        int length = P27.RemoveElement(nums, val);
        
        // Assert
        Assert.Equal(expected, nums);
        Assert.Equal(expectedLength, length);
    }
}