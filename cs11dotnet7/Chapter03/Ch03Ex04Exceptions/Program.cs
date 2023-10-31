Write("Enter a number between 0 and 255: ");
string num1 = ReadLine()!;
Write("Enter another number between 0 and 255: ");
string num2 = ReadLine()!;

try
{
    byte dividend = byte.Parse(num1);
    byte divisor = byte.Parse(num2);
    WriteLine($"{dividend} divided by {divisor} is {dividend/divisor}");
}
catch(DivideByZeroException d)
{
    WriteLine($"{d.GetType()}");
}
catch(FormatException f)
{
    WriteLine($"{f.GetType()}");
}
catch (Exception e)
{
    WriteLine($"{e.GetType()}: {e.Message}");
}