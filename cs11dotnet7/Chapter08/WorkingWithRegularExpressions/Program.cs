using System.Diagnostics.CodeAnalysis; // [StringSyntaxAttribute]

/*
 * Checking for digits entered as text
 */
using System.Text.RegularExpressions;
using System.Xml;

Write("Enter your age: ");
string input = ReadLine()!; // null-forgiving

// Only checks if there is a single digit - doesn't specify what can be entered before or after the digit
// Regex ageChecker = new(@"\d");

// Ensure that we specify the start and end of the string as a number - fails for 2 or more digits
// Regex ageChecker = new(@"^\d$");

// Allow for one or more digits
// Regex ageChecker = new(@"^\d+$");
// Regex ageChecker = new(digitsOnlyText);
Regex ageChecker = DigitsOnly(); // using source generator


if (ageChecker.IsMatch(input))
{
    WriteLine("Thank you!");
}
else
{
    WriteLine($"This is not a valid age: {input}");
}
WriteLine();

/*
 * Splitting a complex comma-separated string
 */
// C# 1 to 10: Use escaped double-quote characters \"
// string films = "\"Monsters, Inc.\",\"I, Tonya\",\"Lock, Stock and Two Smoking Barrels\"";

// C# 11 or later: Use """ to start and end a raw string literal
string films = """
"Monsters, Inc.","I, Tonya","Lock, Stock and Two Smoking Barrels"
""";

WriteLine($"Films to split: {films}");

string[] filmsDumb = films.Split(',');

WriteLine("Splitting with string.Split method:");
foreach (string film in filmsDumb)
{
    WriteLine(film);
}
WriteLine();

// Regex csv = new("(?:^|,)(?=[^\"]|(\")?)\"?((?(1)[^\"]*|[^,\"]*))\"?(?=,|$)");
// Regex csv = new(commaSeparatorText);
Regex csv = CommaSeparator(); // using source generator

MatchCollection filmsSmart = csv.Matches(films);

WriteLine("Splitting with regular expression:");
foreach (Match film in filmsSmart)
{
    WriteLine(film.Groups[2].Value);
}