namespace Math.Test;

public class P412Tests
{
    [Fact]
    public void Test1()
    {
        // Arrange
        int n = 3;
        List<string> expected = new() { "1", "2", "Fizz" };

        // Act
        IList<string> actual = P412.FizzBuzz(n);

        // Assert
        Assert.Equal(expected, actual);
    }

    [Fact]
    public void Test2()
    {
        // Arrange
        int n = 5;
        List<string> expected = new() { "1", "2", "Fizz", "4", "Buzz" };

        // Act
        IList<string> actual = P412.FizzBuzz(n);

        // Assert
        Assert.Equal(expected, actual);
    }

    [Fact]
    public void Test3()
    {
        // Arrange
        int n = 15;
        List<string> expected = new() { "1", "2", "Fizz", "4", "Buzz", "Fizz", "7", "8", "Fizz", "Buzz", "11", "Fizz", "13", "14", "FizzBuzz" };

        // Act
        IList<string> actual = P412.FizzBuzz(n);

        // Assert
        Assert.Equal(expected, actual);
    }
}