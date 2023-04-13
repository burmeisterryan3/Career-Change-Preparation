using System.ComponentModel.DataAnnotations;

namespace Ch06Ex02Inheritance.Shape;

public class Square : Rectangle
{
    public Square(double length) : base(height: length, width: length) { }

    public override double Area => Height * Width;
}
