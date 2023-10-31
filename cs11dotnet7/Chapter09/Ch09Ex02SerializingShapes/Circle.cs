namespace Serializing.Shape;

public class Circle : Shape
{
    /*
     * Properties
     */
    public double Radius { get; init; }
    public override double Area
    {
        get
        {
            return Math.PI * Math.Pow(Radius, 2);
        }
    }
}
