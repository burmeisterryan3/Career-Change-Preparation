/*
 * while Statement
 */
int x = 0;
while (x < 10)
{
    WriteLine(x);
    x++;
}

/*
 * do Statement
 */
string? password;
do
{
    Write("Enter your password: ");
    password = ReadLine();
}
while (password != "Pa$$w0rd");
WriteLine("Correct!");

/*
 * for Statement
 */
for (int y = 1; y <= 10; y++)
{
    WriteLine(y);
}

/*
 * foreach Statement
 */
string[] names = { "Adam", "Barry", "Charlie" };
foreach (string name in names)
{
    WriteLine($"{name} has {name.Length} characters.");
}