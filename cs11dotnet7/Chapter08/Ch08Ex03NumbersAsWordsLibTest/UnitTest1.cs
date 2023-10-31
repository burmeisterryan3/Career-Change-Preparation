using NumbersToWordsLib;
using System.Numerics;

namespace Ch08Ex03NumbersAsWordsLibTest
{
    public class NumbersAsWordsUnitTests
    {
        [Fact]
        public void Test_Int32_0()
        {
            // arrange
            int test = 0;
            string expected = "zero";

            // act
            string actual = test.ToWords();

            // assert
            Assert.Equal(expected, actual);
        }

        [Fact]
        public void Test_Int32_18000000()
        {
            // arrange
            int test = 18000000;
            string expected = "eighteen million";

            // act
            string actual = test.ToWords();

            // assert
            Assert.Equal(expected, actual);
        }

        [Fact]
        public void Test_Int32_1234()
        {
            // arrange
            int test = 1234;
            string expected = "one thousand, two hundred thirty-four";

            // act
            string actual = test.ToWords();

            // assert
            Assert.Equal(expected, actual);
        }

        [Fact]
        public void Test_BigInteger_18456002032011000007()
        {
            // arrange
            BigInteger test = BigInteger.Parse("18456002032011000007");
            string expected = "eighteen quintillion, four hundred fifty-six quadrillion, two trillion, thirty-two billion, eleven million, seven";

            // act
            string actual = test.ToWords();

            // assert
            Assert.Equal(expected, actual);
        }

        [Fact]
        public void Test_Int32_Neg_13()
        {
            // arrange
            int test = -13;
            string expected = "negative thirteen";

            // act
            string actual = test.ToWords();

            // assert
            Assert.Equal(expected, actual);
        }
    }
}