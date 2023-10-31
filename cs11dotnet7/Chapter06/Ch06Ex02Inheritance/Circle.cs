namespace Ch06Ex02Inheritance.Shape;

public class Circle : Square
{
    public Circle(double radius) : base(radius * 2) { }

    public override double Area => Math.PI * Math.Pow(Width / 2, 2);
}
