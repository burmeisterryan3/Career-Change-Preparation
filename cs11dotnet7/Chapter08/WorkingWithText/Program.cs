/*
 * Getting the length of a string
 */
string city = "London";
WriteLine($"{city} is {city.Length} characters long.");

/*
 * Getting the characters of a string
 */
WriteLine($"First char is {city[0]} and fourth is {city[3]}.");

/*
 * Splitting a string
 */
string cities = "Paris,Tehran,Chennai,Sydney,New York,Medellín";

string[] citiesArray = cities.Split(',');

WriteLine($"There are {citiesArray.Length} items in the array:");

foreach (string item in citiesArray)
{
    WriteLine(item);
}

/*
 * Getting part of a string
 */
string fullName = "Alan Shore";

int indexOfTheSpace = fullName.IndexOf(' ');

string firstName = fullName.Substring(
    startIndex: 0, length: indexOfTheSpace);

string lastName = fullName.Substring(
    startIndex: indexOfTheSpace + 1);

WriteLine($"Original: {fullName}");
WriteLine($"Swapped: {lastName}, {firstName}");

/*
 * Checking a string for content
 */
string company = "Microsoft";
bool startsWithM = company.StartsWith("M");
bool containsN = company.Contains("N");

WriteLine($"Text: {company}");
WriteLine($"Starts with M: {startsWithM}, contains an N: {containsN}");

/*
 * Additional methods
 */
string recombined = string.Join("=>", citiesArray);
WriteLine(recombined);

