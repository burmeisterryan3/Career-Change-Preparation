namespace Ch06Ex02Inheritance.Shape;

public abstract class Shape
{
    public double Height { get; init; }
    public double Width { get; init; }
    public abstract double Area { get; }
}