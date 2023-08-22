namespace Arrays.Test;

public class P26Tests
{
    [Fact]
    public void Test1()
    {
        // Arrange
        int[] nums = { 1, 1, 2 };
        int[] expected = { 1, 2, 2 };
        int expectedLength = 2;
        
        // Act
        int length = P26.RemoveDuplicates(nums);
        
        // Assert
        Assert.Equal(expected, nums);
        Assert.Equal(expectedLength, length);
    }

    [Fact]
    public void Test2()
    {
        // Arrange
        int[] nums = { 0, 0, 1, 1, 1, 2, 2, 3, 3, 4 };
        int[] expected = { 0, 1, 2, 3, 4, 2, 2, 3, 3, 4 };
        int expectedLength = 5;
        
        // Act
        int length = P26.RemoveDuplicates(nums);
        
        // Assert
        Assert.Equal(expected, nums);
        Assert.Equal(expectedLength, length);
    }
}