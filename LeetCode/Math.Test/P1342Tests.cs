namespace Math.Test;

public class P1342Tests
{
    [Fact]
    public void Test1()
    {
        // Arrange
        int n = 14;
        int actual = 6;

        // Act
        int result = P1342.NumberOfSteps(n);

        // Assert
        Assert.Equal(actual, result);
    }

    [Fact]
    public void Test2()
    {
        // Arrange
        int n = 8;
        int actual = 4;

        // Act
        int result = P1342.NumberOfSteps(n);

        // Assert
        Assert.Equal(actual, result);
    }

    [Fact]
    public void Test3()
    {
        // Arrange
        int n = 123;
        int actual = 12;

        // Act
        int result = P1342.NumberOfSteps(n);

        // Assert
        Assert.Equal(actual, result);
    }
}