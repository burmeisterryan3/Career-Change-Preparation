﻿using System.Xml.Serialization;

namespace Packt.Shared;

public class Person
{
    public Person() { }
    public Person(decimal initialSalary)
    {
        Salary = initialSalary;
    }

    // Without shortened attribute names, resulting number of bytes is nearly 2x as large
    [XmlAttribute("fname")]
    public string? FirstName { get; set; }
    [XmlAttribute("lname")]
    public string? LastName { get; set; }
    [XmlAttribute("dob")]
    public DateTime DateOfBirth { get; set; }
    public HashSet<Person> Children { get; set; }
    protected decimal Salary { get; set; }
}
