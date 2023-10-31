using System.IO;
using System.Xml;
using static System.Environment; // CurrentDirectory
using static System.IO.Path;

/*
 * Working with Text Streams
 */
SectionTitle("Writing to text streams");

// define a file to write to
string textFile = Combine(CurrentDirectory, "streams.txt");

// create a text file and return a helper writer
StreamWriter text = File.CreateText(textFile);

// enumerate the strings, writing each one
// to the stream on a separate line
foreach (string item in Viper.Callsigns)
{
    text.WriteLine(item);
}
text.Close(); // release resources

// output the contents of the file
WriteLine("{0} contains {1:N0} bytes.",
    arg0: textFile,
    arg1: new FileInfo(textFile).Length);

WriteLine(File.ReadAllText(textFile));

/*
 * Writing to XML Streams
 */
SectionTitle("Writing to XML streams");

// define a file path to write to
string xmlFile = Combine(CurrentDirectory, "streams.xml");

// declare variables for the filestream and XML writer
FileStream? xmlFileStream = null;
XmlWriter? xml = null;

try
{
    // create a file stream
    xmlFileStream = File.Create(xmlFile);

    // wrap the file stream in an XML writer helper
    // and automatically indent nested elements
    xml = XmlWriter.Create(xmlFileStream, new XmlWriterSettings { Indent = true });

    // write the XML declaration
    xml.WriteStartDocument();

    // write a root element
    xml.WriteStartElement("callsigns");

    // enumerate the strings, writing each one to the stream
    foreach (string item in Viper.Callsigns)
    {
        xml.WriteElementString("callsign", item);
    }

    // write the close root element
    xml.WriteEndElement();

    // close helper and stream
    xml.Close();
    xmlFileStream.Close();
}
catch (Exception ex)
{
    // if the path doesn't exist the exception will be caught
    WriteLine($"{ex.GetType()} says {ex.Message}");
}
finally
{
    if (xml != null)
    {
        xml.Dispose();
        WriteLine("The XML writer's unmanaged resources have been disposed.");
    }
    if (xmlFileStream != null)
    {
        xmlFileStream.Dispose();
        WriteLine("The file stream's unmanaged resources have been disposed.");
    }
}

// output all the contents of the file
WriteLine("{0} contains {1:N0} bytes.",
    arg0: xmlFile,
    arg1: new FileInfo(xmlFile).Length);
WriteLine(File.ReadAllText(xmlFile));

/*
 * Simplifying Disposal
 */
/*
string path2 = Combine(CurrentDirectory, "file2.txt");

using (FileStream file2 = File.OpenWrite(path2))
{
    using (StreamWriter writer2 = new StreamWriter(file2))
    {
        try
        {
            writer2.WriteLine("Welcome, .NET!");
        }
        catch (Exception ex)
        {
            WriteLine($"{ex.GetType()} says {ex.Message}");
        }
    } // automatically calls Dispose if the object is not null
} // automatically calls Dispose if the object is not null

File.Delete(path2);
WriteLine($"Does it exist? {File.Exists(path2)}");
*/

/*
 * Simplifying Disposal Even Further
 */
/*
string path3 = Combine(CurrentDirectory, "file3.txt");

using FileStream file3 = File.OpenWrite(path3);
using StreamWriter writer3 = new(file3);

try
{
    writer3.WriteLine("Welcome, .NET!");
}
catch (Exception ex)
{
    WriteLine($"{ex.GetType()} says {ex.Message}");
}

File.Delete(path3);
WriteLine($"Does it exist? {File.Exists(path3)}");
*/

/*
 * Compressing Streams
 */
SectionTitle("Compressing streams");

Compress(algorithm: "gzip");
Compress(algorithm: "brotli");