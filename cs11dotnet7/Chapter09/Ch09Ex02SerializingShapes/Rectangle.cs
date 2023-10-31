namespace Serializing.Shape;

public class Rectangle : Shape
{
    /*
     * Properties
     */
    public double Height { get; init; }
    public double Width { get; init; }
    public override double Area
    {
        get
        {
            return Height * Width;
        }
    }
}
