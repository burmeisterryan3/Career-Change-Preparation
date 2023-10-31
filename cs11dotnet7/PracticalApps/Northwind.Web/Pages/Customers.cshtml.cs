using Packt.Shared; // NorthwindContext, Customer
using Microsoft.AspNetCore.Mvc; // [BindProperty]
using Microsoft.AspNetCore.Mvc.RazorPages; // PageModel

namespace Northwind.Web.Pages;

public class CustomersModel : PageModel
{
    private readonly NorthwindContext db;

    public CustomersModel(NorthwindContext injectedContext)
    {
        db = injectedContext;
    }

    [BindProperty]
    public Customer? Customer { get; set; }
    public IEnumerable<Customer>? Customers { get; set; }

    public void OnGet()
    {
        Customers = db.Customers.OrderBy(c => c.Country).ThenBy(c => c.CompanyName);
    }
}
