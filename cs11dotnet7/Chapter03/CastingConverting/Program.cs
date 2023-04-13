/*
 * Casing int to double - safe
 */
using static System.Convert;

int a = 10;
double b = a; // an int can be safely cast into a double
WriteLine(b);

/*
 * Casting double and long to int - compiler error for implicit cast
 */
double c = 9.8;
// int d = c; // compiler gives an error for this line
int d = (int)c;
WriteLine(d);

long e = 10;
int f = (int)e;
WriteLine($"e is {e:N0} and f is {f:N0}");

e = long.MaxValue;
f = (int)e;
WriteLine($"e is {e:N0} and f is {f:N0}");

e = 5_000_000_000;
f = (int)e;
WriteLine($"e is {e:N0} and f is {f:N0}");

Separate();

/*
 * Using System.Convert
 */
double g = 9.8;
int h = ToInt32(g); // a method of System.Convert
WriteLine($"g is {g} and h is {h}");

Separate();

/*
 * Rounding numbers
 */
double[] doubles = new[] { 9.49, 9.5, 9.51, 10.49, 10.5, 10.51 };
foreach (double n in doubles)
{
    WriteLine($"ToInt32({n}) is {ToInt32(n)}");
}

foreach (double n in doubles)
{
    WriteLine(
      format:"Math.Round({0}, 0, MidpointRounding.AwayFromZero) is {1}",
      arg0: n,
      arg1: Math.Round(value: n, digits: 0, mode: MidpointRounding.AwayFromZero));
}

Separate();

/*
 * ToString
 */
int number = 12;
WriteLine(number.ToString());
bool boolean = true;
WriteLine(boolean.ToString());
DateTime now = DateTime.Now;
WriteLine(now.ToString());
object me = new();
WriteLine(me.ToString());

Separate();

/*
 * Binary ToBase64String
 */
// allocate array of 128 bytes
byte[] binaryObject = new byte[128];

// populate array with random bytes
Random.Shared.NextBytes(binaryObject);

WriteLine("Binary Object as bytes:");
for (int index = 0; index < binaryObject.Length; index++)
{
    Write($"{binaryObject[index]:X} ");
}
WriteLine();

// convert to Base64 string and output as text
string encoded = ToBase64String(binaryObject);
WriteLine($"Binary Object as Base64: {encoded}");

Separate();

/*
 * TryParse
 */
Write("How many eggs are there? ");
string? input = ReadLine(); // or use "12" in notebook
if (int.TryParse(input, out int count))
{
    WriteLine($"There are {count} eggs.");
}
else
{
    WriteLine("I could not parse the input.");
}

void Separate()
{
    WriteLine();
    WriteLine();
}

