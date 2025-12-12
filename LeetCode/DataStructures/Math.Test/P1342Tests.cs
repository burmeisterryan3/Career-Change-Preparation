namespace Math.Test;

public class P1342Tests
{
    [Fact]
    public void Test1()
    {
        // Arrange
        int n = 14;
        int expected = 6;

        // Act
        int actual = P1342.NumberOfSteps(n);

        // Assert
        Assert.Equal(expected, actual);
    }

    [Fact]
    public void Test2()
    {
        // Arrange
        int n = 8;
        int expected = 4;

        // Act
        int actual = P1342.NumberOfSteps(n);

        // Assert
        Assert.Equal(expected, actual);
    }

    [Fact]
    public void Test3()
    {
        // Arrange
        int n = 123;
        int expected = 12;

        // Act
        int actual = P1342.NumberOfSteps(n);

        // Assert
        Assert.Equal(expected, actual);
    }
}