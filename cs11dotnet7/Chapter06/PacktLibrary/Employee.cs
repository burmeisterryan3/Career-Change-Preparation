namespace Packt.Shared;

public class Employee : Person
{
    /*
     * PROPERTIES
     */
    public string? EmployeeCode { get; set; }
    public DateTime HireDate { get; set; }


    /*
     * METHODS
     */
    public override string ToString()
    {
        return $"{Name}'s code is {EmployeeCode}";
    }

    // new keyword indiates we are deliberately replacing old method
    // alternatively, make WriteToConsole virtual in base class and override here
    public new void WriteToConsole()
    {
        WriteLine(format:
            "{0} was born on {1:dd/MM/yy} and hired on {2:dd/MM/yy}",
            arg0: Name,
            arg1: DateOfBirth,
            arg2: HireDate);
    }
}
