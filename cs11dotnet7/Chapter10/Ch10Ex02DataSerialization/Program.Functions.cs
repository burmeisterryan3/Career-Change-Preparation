using Packt.Shared; // Category, Product

using System.Xml; // XmlWriter
using System.Text.Json; // JsonSerializer

using static System.IO.Path; // Combine
using static System.Environment; // CurrentDirectory

delegate void WriteDataDelegate(string name, string? value);

partial class Program
{
    static void SerializeDbToJson(IQueryable<Category> categories)
    {
        string filePath = Combine(CurrentDirectory, "northwind-serialized.json");

        using (FileStream jsonStream = File.Create(filePath))
        {
            // Setting Indented = false cuts the size of the Json file by nearly 50%
            using (Utf8JsonWriter jsonWriter = new Utf8JsonWriter(jsonStream, new JsonWriterOptions { Indented = true }))
            {
                jsonWriter.WriteStartObject();
                jsonWriter.WriteStartArray("categories");

                foreach (Category c in categories)
                {
                    jsonWriter.WriteStartObject();

                    jsonWriter.WriteNumber("id", c.CategoryId);
                    jsonWriter.WriteString("name", c.CategoryName);
                    jsonWriter.WriteString("description", c.Description);
                    jsonWriter.WriteNumber("product_count", c.Products.Count);

                    jsonWriter.WriteStartArray("products");

                    foreach (Product p in c.Products)
                    {
                        jsonWriter.WriteStartObject();

                        jsonWriter.WriteNumber("id", p.ProductId);
                        jsonWriter.WriteString("name", p.ProductName);
                        jsonWriter.WriteNumber("cost", p.Cost is null  ? 0 : p.Cost.Value);
                        jsonWriter.WriteNumber("stock", p.Stock is null ? 0 : p.Stock.Value);
                        jsonWriter.WriteBoolean("discontinued", p.Discontinued);

                        jsonWriter.WriteEndObject(); // product
                    }

                    jsonWriter.WriteEndArray(); // products
                    jsonWriter.WriteEndObject(); // category
                }
                jsonWriter.WriteEndArray(); // categories
                jsonWriter.WriteEndObject();
            }
        }

        WriteFileNameAndSize(filePath);
    }

    static void SerializeDbToXml(IQueryable<Category> categories, bool useAttributes = true)
    {
        string which = useAttributes ? "attributes" : "elements";
        string filePath = $"northwind-serialized-{which}.xml";

        using (FileStream xmlStream = File.Create(filePath))
        {
            using (XmlWriter xml =  XmlWriter.Create(xmlStream, new XmlWriterSettings { Indent = true }))
            {
                WriteDataDelegate writeMethod = useAttributes ? xml.WriteAttributeString : xml.WriteElementString;

                xml.WriteStartDocument();
                xml.WriteStartElement("categories");

                foreach (Category c in categories)
                {
                    xml.WriteStartElement("category");
                    writeMethod("id", c.CategoryId.ToString());
                    writeMethod("name", c.CategoryName);
                    writeMethod("description", c.Description);
                    writeMethod("product_count", c.Products.Count.ToString());
                    xml.WriteStartElement("products");

                    foreach (Product p in c.Products)
                    {
                        xml.WriteStartElement("product");
                        
                        writeMethod("id", p.ProductId.ToString());
                        writeMethod("name", p.ProductName);
                        writeMethod("cost", p.Cost is null ? "0" : p.Cost.Value.ToString());
                        writeMethod("stock", p.Stock is null ? "0" : p.Stock.Value.ToString());
                        writeMethod("discontinued", p.Discontinued.ToString());

                        xml.WriteEndElement(); // </product>
                    }
                    xml.WriteEndElement(); // </products>
                    xml.WriteEndElement(); // </category>
                }
                xml.WriteEndElement(); // </categories>
                xml.WriteEndDocument();
            }
        }

        WriteFileNameAndSize(filePath);
    }

    static void SerializeDbToCsv(IQueryable<Category> categories)
    {
        string filePath = Combine(CurrentDirectory, "northwind-serialized.csv");

        using (FileStream csvStream = File.Create(filePath))
        {
            using (StreamWriter csv = new(csvStream))
            {
                csv.WriteLine("CategoryId,CategoryName,Description,ProductId,ProductName,Cost,Stock,Discontinued");

                foreach (Category c in categories)
                {
                    foreach (Product p in c.Products)
                    {
                        csv.Write("{0},\"{1}\",\"{2}\",",
                          arg0: c.CategoryId,
                          arg1: c.CategoryName,
                          arg2: c.Description);

                        csv.Write("{0},\"{1}\",{2},",
                          arg0: p.ProductId,
                          arg1: p.ProductName,
                          arg2: p.Cost is null ? 0 : p.Cost.Value);

                        csv.WriteLine("{0},{1}",
                          arg0: p.Stock is null ? 0 : p.Stock.Value,
                          arg1: p.Discontinued);
                    }
                }
            }
        }

        WriteFileNameAndSize(filePath);
    }

    static void WriteFileNameAndSize(string filePath)
    {
        WriteLine("{0} is {1:N0} bytes",
            arg0: filePath,
            arg1: new FileInfo(filePath).Length);
        WriteLine();
    }
}
