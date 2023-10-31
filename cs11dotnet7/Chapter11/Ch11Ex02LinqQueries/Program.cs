using Packt.Shared; // Northwind, Category, Product

using (Northwind db = new())
{

    IQueryable<string?> distinctCities = db.Customers.Select(c => c.City).Distinct();
    
    WriteLine("Cities where customers currently reside: ");
    WriteLine($"{String.Join(", ", distinctCities)}");
    WriteLine();

    Write("Enter the name of a city: ");
    string city = ReadLine()!;

    IQueryable<Customer> customersInCity = db.Customers.Where(c => c.City == city);

    if (!customersInCity.Any())
    {
        WriteLine($"No customers in {city}.");
        return;
    }

    WriteLine($"There are {customersInCity.Count()} customers in {city}:");

    foreach (Customer c in customersInCity)
    {
        WriteLine($"{c.CompanyName}");
    }
}
