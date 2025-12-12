namespace Arrays.Test;

public class P1089Tests
{
    [Fact]
    public void Test1()
    {
        // Arrange
        int[] ints = { 1, 0, 2, 3, 0, 4, 5, 0 };
        int[] expected = { 1, 0, 0, 2, 3, 0, 0, 4 };
        
        // Act
        P1089.DuplicateZeros(ints);
        
        // Assert
        Assert.Equal(expected, ints);
    }

   [Fact]
    public void Test2()
    {
        // Arrange
        int[] ints = { 1, 2, 3 };
        int[] expected = { 1, 2, 3 };
        
        // Act
        P1089.DuplicateZeros(ints);
        
        // Assert
        Assert.Equal(expected, ints);
    }
}