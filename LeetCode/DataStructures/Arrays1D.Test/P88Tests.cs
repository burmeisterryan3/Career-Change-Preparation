namespace Arrays.Test;

public class P88Tests
{
    [Fact]
    public void Test1()
    {
        // Arrange
        int[] nums1 = { 1, 2, 3, 0, 0, 0 };
        int m = 3;
        int[] nums2 = { 2, 5, 6 };
        int n = 3;
        int[] expected = { 1, 2, 2, 3, 5, 6 };
        
        // Act
        P88.Merge(nums1, m, nums2, n);
        
        // Assert
        Assert.Equal(expected, nums1);
    }

    [Fact]
    public void Test2()
    {
        // Arrange
        int[] nums1 = { 1 };
        int m = 1;
        int[] nums2 = { };
        int n = 0;
        int[] expected = { 1 };
        
        // Act
        P88.Merge(nums1, m, nums2, n);
        
        // Assert
        Assert.Equal(expected, nums1);
    }

        [Fact]
    public void Test3()
    {
        // Arrange
        int[] nums1 = { 0 };
        int m = 0;
        int[] nums2 = { 1 };
        int n = 1;
        int[] expected = { 1 };
        
        // Act
        P88.Merge(nums1, m, nums2, n);
        
        // Assert
        Assert.Equal(expected, nums1);
    }
}