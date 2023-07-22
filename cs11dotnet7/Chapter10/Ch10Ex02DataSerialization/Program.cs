using Packt.Shared;

using Microsoft.EntityFrameworkCore;

SectionTitle("");

using (Northwind db = new())
{
    IQueryable<Category>? categories = db.Categories?.Include(c => c.Products);

    if (categories is null)
    {
        Fail("There are no categories.");
        return;
    }

    SectionTitle("Serializing to JSON");
    SerializeDbToJson(categories);

    SectionTitle("Serializing to XML - with Attributes");
    SerializeDbToXml(categories);

    SectionTitle("Serializing to XML - with Elements");
    SerializeDbToXml(categories, false);

    SectionTitle("Serializing to CSV");
    SerializeDbToCsv(categories);
}