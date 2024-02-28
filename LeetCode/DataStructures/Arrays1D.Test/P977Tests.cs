namespace Arrays.Test;

public class P977Tests
{
    [Fact]
    public void Test1()
    {
        // Arrange
        int[] ints = { -4, -1, 0, 3, 10 };
        int[] expected = { 0, 1, 9, 16, 100 };
        
        // Act
        int[] result = P977.SortedSquares(ints);
        
        // Assert
        Assert.Equal(expected, result);
    }

   [Fact]
    public void Test2()
    {
        // Arrange
        int[] ints = { -7, -3, 2, 3, 11 };
        int[] expected = { 4, 9, 9, 49, 121 };
        
        // Act
        int[] result = P977.SortedSquares(ints);
        
        // Assert
        Assert.Equal(expected, result);
    }

    [Fact]
    public void Test3()
    {
        // Arrange
        int[] ints = { -1 };
        int[] expected = { 1 };
        
        // Act
        int[] result = P977.SortedSquares(ints);
        
        // Assert
        Assert.Equal(expected, result);
    }

    [Fact]
    public void Test4()
    {
        // Arrange
        int[] ints = { -5, -3, -2, -1 };
        int[] expected = { 1, 4, 9, 25 };
        
        // Act
        int[] actual = P977.SortedSquares(ints);
        
        // Assert
        Assert.Equal(expected, actual);
    }
}