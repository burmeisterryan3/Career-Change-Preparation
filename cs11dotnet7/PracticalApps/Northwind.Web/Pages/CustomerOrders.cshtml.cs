using Packt.Shared; // NorthwindContext, Customer
using Microsoft.AspNetCore.Mvc; // [BindProperty]
using Microsoft.EntityFrameworkCore; // Include
using Microsoft.AspNetCore.Mvc.RazorPages; // PageModel

namespace Northwind.Web.Pages;

public class CustomerOrdersModel : PageModel
{
    private readonly NorthwindContext db;

    public CustomerOrdersModel(NorthwindContext injectedContext)
    {
        db = injectedContext;
    }

    [BindProperty]
    public Customer? Customer { get; set; }

    public void OnGet()
    {
        string id = HttpContext.Request.Query["id"]!;

        Customer = db.Customers.Include(c => c.Orders).SingleOrDefault(c => c.CustomerId == id);
    }
}
