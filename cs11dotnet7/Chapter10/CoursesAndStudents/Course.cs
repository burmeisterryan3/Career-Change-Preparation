using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace Packt.Shared;

public class Course
{
    [Key]
    public int CourseId { get; set; }

    [Required]
    [StringLength(60)]
    public string? Title { get; set; }

    [InverseProperty("Courses")]
    public ICollection<Student>? Students { get; set; }
}
