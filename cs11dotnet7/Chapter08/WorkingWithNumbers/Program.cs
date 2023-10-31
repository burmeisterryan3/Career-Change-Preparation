using System.Numerics;

/*
 * Working with Big Integers
 */
WriteLine("Working with large integers:");
WriteLine("---------------------------------");

ulong big = ulong.MaxValue;
WriteLine($"{big,40:N0}"); // 40 = right-align 40 characters, line up to right-hand edge

BigInteger bigger = BigInteger.Parse("123456789012345678901234567890");
WriteLine($"{bigger,40:N0}"); // line up to right-hand edge

/*
 * Working with Complex Numbers
 */
WriteLine("Working with complex numbers:");

Complex c1 = new(real: 4, imaginary: 2);
Complex c2 = new(real: 3, imaginary: 7);
Complex c3 = c1 + c2;

// output using default ToString implementation
WriteLine($"{c1} added to {c2} is {c3}");

// output using custom format
WriteLine("{0} + {1}i added to {2} + {3}i is {4} + {5}i",
    c1.Real, c1.Imaginary,
    c2.Real, c2.Imaginary,
    c3.Real, c3.Imaginary);

/*
 * Working with Random Numbers (non-cryptographic scenarios)
 */
Random r = new();
Random r2 = new(Seed: 46738);
Random r3 = Random.Shared; // .NET 6

// minValue is an inclusive lower bound, i.e. 1 is a possible value
// maxValue is an exclusive upper bound, i.e. 7 is NOT a possible value
int dieRoll = r3.Next(minValue: 1, maxValue: 7);  // returns 1 to 6
WriteLine($"{dieRoll}");

double randomReal = r.NextDouble(); // returns 0.0. to less than 1.0
WriteLine($"{randomReal}");

byte[] arrayOfBytes = new byte[256];
r.NextBytes(arrayOfBytes); // 256 random bytes in an array
WriteLine($"First Byte: {arrayOfBytes[0]}");
WriteLine($"Last Byte: {arrayOfBytes[255]}");
