using System.Threading;

namespace Packt.Shared;

public class Person : Object, IComparable<Person?>
{
    /*
     * FIELDS
     */
    public event EventHandler? Shout;
    public int AngerLevel;

    /*
     * PROPERTIES
     */
    public string? Name { get; set; }
    public DateTime DateOfBirth { get; set; }

    /*
     * METHODS
     */
    public override string ToString()
    {
        return $"{Name} is a {base.ToString()}";
    }
    public void WriteToConsole()
    {
        WriteLine($"{Name} was born on a {DateOfBirth:dddd}.");
    }

    public void Poke()
    {
        AngerLevel++;
        if (AngerLevel >= 3)
        {
            // if something is listening, call the delegate
            Shout?.Invoke(this, EventArgs.Empty);

            // Same as...
            // if (Shout != null)
            //     Shout(this, EventArgs.Empty);
        }
    }

    public void TimeTravel(DateTime when)
    {
        if (when <= DateOfBirth)
        {
            throw new PersonException("If you travel back in time to a date" + 
                " earlier than your own birth, then the universe will explode!");
        }
        else
        {
            WriteLine($"Welcome to {when:yyyy}!");
        }
    }

    /*
     * INTERFACE IMPLEMENTATIONS
     */
    public int CompareTo(Person? other)
    {
        int position;
        if ((this is not null) && (other is not null))
        {
            if ((Name is not null) && (other.Name is not null))
            {
                // if both Name values are not null,
                // use the string implementation of CompareTo
                position = Name.CompareTo(other.Name);
            } 
            else if ((Name is not null) && (other.Name is null))
            {
                position = -1; // this Person precedes other Person
            }
            else if ((Name is null) && (other.Name is not null))
            {
                position = 1; // this Person follows other Person
            }
            else
            {
                position = 0;
            }
        }
        else if ((this is not null) && (other is null))
        {
            position = -1; // this Person precedes other Person
        }
        else if ((this is null) && (other is not null))
        {
            position = 1; // this Person follows other Person
        }
        else
        {
            position = 0;
        }

        return position;
    }
}