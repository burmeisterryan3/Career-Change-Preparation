using Ch04Ex02PrimeFactorsLib;

namespace PrimeFactorsLibUnitTests
{
    public class PrimeFactorsUnitTests
    {
        [Fact]
        public void TestFactoring0()
        {
            //arrange
            int num = 0;
            string expected = "Prime factors of 0 are: 0";
            PrimeFactors pf = new();

            //act
            string actual = pf.Factorize(num);

            // assert
            Assert.Equal(expected, actual);
        }

        [Fact]
        public void TestFactoring1()
        {
            //arrange
            int num = 1;
            string expected = "Prime factors of 1 are: 1";
            PrimeFactors pf = new();

            //act
            string actual = pf.Factorize(num);

            // assert
            Assert.Equal(expected, actual);
        }

        [Fact]
        public void TestFactoring2()
        {
            //arrange
            int num = 2;
            string expected = "Prime factors of 2 are: 2";
            PrimeFactors pf = new();

            //act
            string actual = pf.Factorize(num);

            // assert
            Assert.Equal(expected, actual);
        }

        [Fact]
        public void TestFactoring19()
        {
            //arrange
            int num = 19;
            string expected = "Prime factors of 19 are: 19";
            PrimeFactors pf = new();

            //act
            string actual = pf.Factorize(num);

            // assert
            Assert.Equal(expected, actual);
        }

        [Fact]
        public void TestFactoring20()
        {
            //arrange
            int num = 20;
            string expected = "Prime factors of 20 are: 5 x 2 x 2";
            PrimeFactors pf = new();

            //act
            string actual = pf.Factorize(num);

            // assert
            Assert.Equal(expected, actual);
        }

        [Fact]
        public void TestFactoring1000() 
        {
            //arrange
            int num = 1000;
            string expected = "Prime factors of 1000 are: 5 x 5 x 5 x 2 x 2 x 2";
            PrimeFactors pf = new();

            //act
            string actual = pf.Factorize(num);

            // assert
            Assert.Equal(expected, actual);
        }

        [Fact]
        public void TestFactoringNeg1() 
        {
            //arrange
            int num = -1;
            string expected = "Prime factors of -1 are: -1";
            PrimeFactors pf = new();

            //act
            string actual = pf.Factorize(num);

            // assert
            Assert.Equal(expected, actual);
        }

        [Fact]
        public void TestFactoringNeg2()
        {
            //arrange
            int num = -2;
            string expected = "Prime factors of -2 are: -2";
            PrimeFactors pf = new();

            //act
            string actual = pf.Factorize(num);

            // assert
            Assert.Equal(expected, actual);
        }

        [Fact]
        public void TestFactoringNeg19()
        {
            //arrange
            int num = -19;
            string expected = "Prime factors of -19 are: -19";
            PrimeFactors pf = new();

            //act
            string actual = pf.Factorize(num);

            // assert
            Assert.Equal(expected, actual);
        }

        [Fact]
        public void TestFactoringNeg20()
        {
            //arrange
            int num = -20;
            string expected = "Prime factors of -20 are: 5 x 2 x -2";
            PrimeFactors pf = new();

            //act
            string actual = pf.Factorize(num);

            // assert
            Assert.Equal(expected, actual);
        }

        [Fact]
        public void TestFactoringNeg1000()
        {
            //arrange
            int num = -1000;
            string expected = "Prime factors of -1000 are: 5 x 5 x 5 x 2 x 2 x -2";
            PrimeFactors pf = new();

            //act
            string actual = pf.Factorize(num);

            // assert
            Assert.Equal(expected, actual);
        }
    }
}