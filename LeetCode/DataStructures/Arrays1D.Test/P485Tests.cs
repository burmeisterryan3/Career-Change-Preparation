namespace Arrays.Test;

public class P485Tests
{
    [Fact]
    public void Test1()
    {
        // Arrange
        int[] ints = { 1, 1, 0, 1, 1, 1 };
        int expected = 3;
        
        // Act
        int actual = P485.FindMaxConsecutiveOnes(ints);
        
        // Assert
        Assert.Equal(expected, actual);
    }

   [Fact]
    public void Test2()
    {
        // Arrange
        int[] ints = { 1, 0, 1, 1, 0, 1 };
        int expected = 2;
        
        // Act
        int actual = P485.FindMaxConsecutiveOnes(ints);
        
        // Assert
        Assert.Equal(expected, actual);
    }
}