/*
 * Overflow permitted
 */
int x = int.MaxValue - 1;
WriteLine($"Initial value: {x}");
x++; // int.MaxValue
WriteLine($"After incrementing: {x}");
x++;
WriteLine($"After incrementing: {x}");
x++;
WriteLine($"After incrementing: {x}");

WriteLine();

/*
 * Have compiler check for overflow
 */
/* Uncomment to see running
checked
{
    x = int.MaxValue - 1;
    WriteLine($"Initial value: {x}");
    x++;
    WriteLine($"After incrementing: {x}");
    x++;
    WriteLine($"After incrementing: {x}");
    x++;
    WriteLine($"After incrementing: {x}");
}

WriteLine();
*/

/*
 * Catch overflow
 */
try
{
    checked
    {
        x = int.MaxValue - 1;
        WriteLine($"Initial value: {x}");
        x++;
        WriteLine($"After incrementing: {x}");
        x++;
        WriteLine($"After incrementing: {x}");
        x++;
        WriteLine($"After incrementing: {x}");
    }
}
catch (OverflowException)
{
    WriteLine("The code overflowed but I caught the exception.");
}

/*
 * Compile-time Checking
 */
// int y = int.MaxValue + 1; // Uncomment this line to see compiler warning

unchecked
{
    int y = int.MaxValue + 1;
    WriteLine($"Initial value: {y}");
    y--;
    WriteLine($"After decrementing: {y}");
    y--;
    WriteLine($"After decrementing: {y}");
}