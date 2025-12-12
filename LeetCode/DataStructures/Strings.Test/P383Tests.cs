namespace Strings.Test;

public class P383Tests
{
    [Fact]
    public void Test1()
    {
        // Arrange
        string ransomNote = "a";
        string magazine = "b";

        // Act
        bool actual = P383.CanConstruct(ransomNote, magazine);

        // Assert
        Assert.False(actual);
    }

    [Fact]
    public void Test2()
    {
        // Arrange
        string ransomNote = "aa";
        string magazine = "ab";

        // Act
        bool actual = P383.CanConstruct(ransomNote, magazine);

        // Assert
        Assert.False(actual);
    }

    [Fact]
    public void Test3()
    {
        // Arrange
        string ransomNote = "aa";
        string magazine = "aab";

        // Act
        bool actual = P383.CanConstruct(ransomNote, magazine);

        // Assert
        Assert.True(actual);
    }
}