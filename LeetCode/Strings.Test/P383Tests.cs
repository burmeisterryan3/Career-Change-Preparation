namespace Strings.Test;

public class P876Tests
{
    [Fact]
    public void Test1()
    {
        // Arrange
        string ransomNote = "a";
        string magazine = "b";

        // Act
        bool result = P383.CanConstruct(ransomNote, magazine);

        // Assert
        Assert.False(result);
    }

    [Fact]
    public void Test2()
    {
        // Arrange
        string ransomNote = "aa";
        string magazine = "ab";

        // Act
        bool result = P383.CanConstruct(ransomNote, magazine);

        // Assert
        Assert.False(result);
    }

    [Fact]
    public void Test3()
    {
        // Arrange
        string ransomNote = "aa";
        string magazine = "aab";

        // Act
        bool result = P383.CanConstruct(ransomNote, magazine);

        // Assert
        Assert.True(result);
    }
}