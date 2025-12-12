namespace Arrays2D.Test;

public class P1672Tests
{
    [Fact]
    public void Test1()
    {
        // Arrange
        int[][] accounts = 
        {
            new int[] { 1, 2, 3 },
            new int[] { 3, 2, 1 }
        };

        int expected = 6;

        // Act
        int result = P1672.MaximumWealth(accounts);

        // Assert
        Assert.Equal(expected, result);
    }

    [Fact]
    public void Test2()
    {
        // Arrange
        int[][] accounts =
        {
            new int[] { 1, 5 },
            new int[] { 7, 3 },
            new int[] { 3, 5 }
        };
        int expected = 10;

        // Act
        int result = P1672.MaximumWealth(accounts);

        // Assert
        Assert.Equal(expected, result);
    }

    [Fact]
    public void Test3()
    {
        // Arrange
        int[][] accounts =
        {
            new int[] { 2, 8, 7 },
            new int[] { 7, 1, 3 }, 
            new int[] { 1, 9, 5 }
        };
        int expected = 17;

        // Act
        int actual = P1672.MaximumWealth(accounts);

        // Assert
        Assert.Equal(expected, actual);
    }
}