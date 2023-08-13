namespace Arrays.Test;

public class P1480Tests
{
    [Fact]
    public void Test1()
    {
        // Arrange
        int[] ints = { 1, 2, 3, 4 };
        int[] actual = { 1, 3, 6, 10 };
        
        // Act
        int[] result = P1480.RunningSum1dArray(ints);
        
        // Assert
        Assert.Equal(actual, result);
    }

    [Fact]
    public void Test2()
    {
        // Arrange
        int[] ints = { 1, 1, 1, 1 };
        int[] actual = { 1, 2, 3, 4, };

        // Act
        int[] result = P1480.RunningSum1dArray(ints);

        // Assert
        Assert.Equal(actual, result);
    }

    [Fact]
    public void Test3()
    {
        // Arrange
        int[] ints = { 3, 1, 2, 10, 1 };
        int[] actual = { 3, 4, 6, 16, 17 }; 

        // Act
        int[] result = P1480.RunningSum1dArray(ints);

        // Assert
        Assert.Equal(actual, result);
    }
}