using System.Xml.Serialization;

namespace Serializing.Shape;

[XmlInclude(typeof(Circle))]
[XmlInclude(typeof(Rectangle))]
public abstract class Shape
{
    /*
     * Fields
     */
    public string? Color { get; init; }
    public abstract double Area { get; }
}
