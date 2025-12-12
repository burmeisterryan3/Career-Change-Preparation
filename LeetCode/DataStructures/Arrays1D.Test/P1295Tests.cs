namespace Arrays.Test;

public class P1295Tests
{
    [Fact]
    public void Test1()
    {
        // Arrange
        int[] ints = { 12, 345, 2, 6, 7896 };
        int expected = 2;
        
        // Act
        int actual = P1295.FindNumbers(ints);
        
        // Assert
        Assert.Equal(expected, actual);
    }

   [Fact]
    public void Test2()
    {
        // Arrange
        int[] ints = { 555, 901, 482, 1771 };
        int expected = 1;
        
        // Act
        int actual = P1295.FindNumbers(ints);
        
        // Assert
        Assert.Equal(expected, actual);
    }
}