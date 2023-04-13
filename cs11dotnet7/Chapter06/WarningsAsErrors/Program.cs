Write("Enter a name: ");
string? name = ReadLine();
if (name == null)
{
    WriteLine("You did not enter a name.");
    return;
}
WriteLine($"Hello, {name} has {name.Length} characters!");