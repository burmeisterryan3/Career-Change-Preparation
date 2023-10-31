using System.Xml.Linq;

namespace Packt.Shared;

public partial class Person
{
    /*
     * FIELDS
     */
    private string? favoriteIceCream;
    private string? favoritePrimaryColor;
    private bool married = false;
    private Person? spouse = null;

    /*
     * PROPERTIES
     */
    public string Origin
    {
        get
        {
            return string.Format("{0} was born on {1}", arg0: Name, arg1: HomePlanet);
        }
    } // C# 1-5 syntax
    public string Greeting => $"{Name} says 'Hello!'"; // Newer syntax
    public int Age => DateTime.Today.Year - DateOfBirth.Year;
    public string? FavoriteIceCream { get; set; } // auto-syntax
    public string? FavoritePrimaryColor
    {
        get
        {
            return favoritePrimaryColor;
        }
        set
        {
            switch (value?.ToLower())
            {
                case "red":
                case "green":
                case "blue":
                    favoritePrimaryColor = value;
                    break;
                default:
                    throw new ArgumentException(
                    $"{value} is not a primary color. Choose from: red, green, blue.");
            }
        }
    }
    public bool Married => married;
    public Person? Spouse => spouse;
    public static void Marry(Person p1, Person p2)
    {
        p1.Marry(p2);
    }
    public void Marry(Person partner)
    {
        if (married) return;
        spouse = partner;
        married = true;
        partner.Marry(this); // this is the current object - perform Marry for other Person as well
    } // instance method
    public static Person Procreate(Person p1, Person p2)
    {
        if (p1.Spouse != p2)
        {
            throw new ArgumentException("You must be married to procreate.");
        }

        Person baby = new()
        {
            Name = $"Baby of {p1.Name} and {p2.Name}",
            DateOfBirth = DateTime.Now
        };

        p1.Children.Add(baby);
        p2.Children.Add(baby);

        return baby;
    }
    public Person ProcreateWith(Person partner)
    {
        return Procreate(this, partner);
    }
    // method with a local function
    public static int Factorial(int number)
    {
        if (number < 0)
        {
            throw new ArgumentException(
            $"{nameof(number)} cannot be less than zero.");
        }
        return localFactorial(number);

        int localFactorial(int localNumber) // local function
        {
            if (localNumber == 0) return 1;
            return localNumber * localFactorial(localNumber - 1);
        }
    }

    /*
     * INDEXERS
     */
    public Person this[int index]
    {
        get
        {
            return Children[index];
        }
        set
        {
            Children[index] = value;
        }
    }
    public Person this[string name]
    {
        get
        {
            return Children.Find(p => p.Name == name);
        }
        set
        {
            Person found = Children.Find(p =>p.Name == name);
            if (found is not null) found = value;
        }
    }

    /*
     * OPERATORS
     */
    // operato to "marry"
    public static bool operator +(Person p1, Person p2)
    {
        Marry(p1, p2);
        return p1.Married && p2.Married; // confirm they are both now married
    }

    // operator to "multiply"
    public static Person operator *(Person p1, Person p2)
    {
        return Procreate(p1, p2);
    }
}
