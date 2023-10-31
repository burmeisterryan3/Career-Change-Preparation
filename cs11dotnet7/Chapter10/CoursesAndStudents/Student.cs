using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace Packt.Shared;

public class Student
{
    [Key]
    public int StudentId { get; set; }

    [StringLength(60)]
    public string? FirstName { get; set; }

    [StringLength(60)]
    public string? LastName { get; set; }
    
    [InverseProperty("Students")]
    public ICollection<Course>? Courses { get; set; }
}
