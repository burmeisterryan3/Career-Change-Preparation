int numberOfApples = 12;
decimal pricePerApple = 0.35M;

WriteLine(
    format: "{0} apples cost {1:C}",
    arg0: numberOfApples,
    arg1: pricePerApple * numberOfApples);

string formatted = string.Format(
    format: "{0} apples cost {1:C}",
    arg0: numberOfApples,
    arg1: pricePerApple * numberOfApples);

//WriteToFile(formatted); // writes the string into a file

/* Four parameter values can use named arguments.
WriteLine(
    format: "{0} {1} lived in {2}, {3}.",
    arg0: "Roger", arg1: "Cevung",
    arg2: "Stockholm", arg3: "Sweden");
*/

// Five or more parameter values cannot use named arguments.
WriteLine(
    format: "{0} {1} lived in {2}, {3} and worked in the {4} team at {5}.",
    "Roger", "Cevung", "Stockholm", "Sweden", "Education", "Optimizely");

// The following statement must be all on one line... Can separate by newlines in C# 11
WriteLine($"{numberOfApples} apples cost {pricePerApple * numberOfApples:C}");

string applesText = "Apples";
int applesCount = 1234;
string bananasText = "Bananas";
int bananasCount = 56789;

WriteLine(
    format: "{0,-10} {1,6}",
    arg0: "Name",
    arg1: "Count");

WriteLine(
    format: "{0,-10} {1,6:N0}",
    arg0: applesText,
    arg1: applesCount);

WriteLine(
    format: "{0,-10} {1,6:N0}",
    arg0: bananasText,
    arg1: bananasCount);

// ReadLine functionality
Write("Type your first name and press ENTER: ");
string firstName = ReadLine()!;

Write("Type your age and press ENTER: ");
string? age = ReadLine();

WriteLine($"Hello {firstName}, you look good for {age}.");

// ReadKey
Write("Press any key combination: ");
ConsoleKeyInfo key = ReadKey();
WriteLine();
WriteLine("Key: {0}, Char: {1}, Modifiers: {2}",
    arg0: key.Key,
    arg1: key.KeyChar,
    arg2: key.Modifiers);