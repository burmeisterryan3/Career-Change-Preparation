namespace Hard.Test;

public class P239Tests
{
    [Fact]
    public void Test1()
    {
        // Arrange
        int[] nums = [1, 3, -1, -3, 5, 3, 6, 7];
        int windowLength = 3;

        int[] expected = [3, 3, 5, 5, 6, 7];

        // Act
        int[] actual = P239.MaxSlidingWindow(nums, windowLength);

        // Assert
        Assert.Equal(expected, actual);
    }

    [Fact]
    public void Test2()
    {
        // Arrange
        int[] nums = [1];
        int windowLength = 1;

        int[] expected = [1];

        // Act
        int[] actual = P239.MaxSlidingWindow(nums, windowLength);

        // Assert
        Assert.Equal(expected, actual);
    }
}