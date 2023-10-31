using System.Xml.Serialization;
using Serializing.Shape; // Shape, Rectangle, Circle

using static System.IO.Path; // Combine
using static System.Environment; // CurrentDirectory

// create a list of Shapes to serialize
List<Shape> listOfShapes = new()
{
    new Circle { Color = "Red", Radius = 2.5 },
    new Rectangle { Color = "Blue", Height = 20.0, Width = 10.0 },
    new Circle { Color = "Green", Radius = 8.0 },
    new Circle { Color = "Purple", Radius = 12.3 },
    new Rectangle { Color = "Blue", Height = 45.0, Width = 18.0 }
};

string path = Combine(CurrentDirectory, "shapes.xml");

SectionTitle("Serializing list of shapes");

XmlSerializer xs = new XmlSerializer(type: listOfShapes.GetType());

using (FileStream xmlFileStream = File.Create(path))
{
    xs.Serialize(xmlFileStream, listOfShapes);
}

WriteLine("Written {0:N0} bytes of XML to {1}",
    arg0: new FileInfo(path).Length,
    arg1: path);
WriteLine();

SectionTitle("Deserializing list of shapes");

using (FileStream xmlFile = File.Open(path, FileMode.Open))
{
    List<Shape>? loadedShapesXml = xs.Deserialize(xmlFile) as List<Shape>;

    foreach (Shape item in loadedShapesXml ?? new List<Shape>())
    {
        WriteLine("{0} is {1} and has an area of {2:N2}",
            item.GetType().Name,
            item.Color,
            item.Area);
    }
}