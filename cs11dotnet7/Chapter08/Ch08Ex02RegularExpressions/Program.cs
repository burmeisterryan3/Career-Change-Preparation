using System.Text.RegularExpressions;

WriteLine("The default regular expression checks for at least one digit.");

do
{
    Write("Enter a regular expression (or press ENTER to use the default): ");
    string? regexp = ReadLine();
    Regex r = regexp is null ? userRegex() : new(regexp);

    Write("Enter some input: ");
    string? input = ReadLine();

    WriteLine($"{input} matches {regexp}? {r.IsMatch(input!)}");

    WriteLine("Press ESC to end or any key to try again.");
} while (ReadKey(intercept: true).Key != ConsoleKey.Escape);