namespace Arrays.Test;

// https://leetcode.com/problems/running-sum-of-1d-array/
public class P1480Tests
{
    [Fact]
    public void Test1()
    {
        // Arrange
        int[] ints = { 1, 2, 3, 4 };
        int[] expected = { 1, 3, 6, 10 };
        
        // Act
        int[] actual = P1480.RunningSum1dArray(ints);
        
        // Assert
        Assert.Equal(expected, actual);
    }

    [Fact]
    public void Test2()
    {
        // Arrange
        int[] ints = { 1, 1, 1, 1 };
        int[] expected = { 1, 2, 3, 4, };

        // Act
        int[] actual = P1480.RunningSum1dArray(ints);

        // Assert
        Assert.Equal(expected, actual);
    }

    [Fact]
    public void Test3()
    {
        // Arrange
        int[] ints = { 3, 1, 2, 10, 1 };
        int[] expected = { 3, 4, 6, 16, 17 }; 

        // Act
        int[] actual = P1480.RunningSum1dArray(ints);

        // Assert
        Assert.Equal(expected, actual);
    }
}