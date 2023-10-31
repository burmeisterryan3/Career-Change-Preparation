using Packt.Shared; // NorthwindContext
using Microsoft.AspNetCore.Mvc; // [BindProperty], IActionResult
using Microsoft.AspNetCore.Mvc.RazorPages; // PageModel

namespace Northwind.Web.Pages
{
    public class SuppliersModel : PageModel
    {
        private readonly NorthwindContext db;

        public SuppliersModel(NorthwindContext injectedContext)
        {
            db = injectedContext;
        }

        [BindProperty]
        public Supplier? Supplier { get; set; }
        public IEnumerable<Supplier>? Suppliers { get; set; }

        public IActionResult OnPost()
        {
            if ((Supplier is not null) && ModelState.IsValid)
            {
                db.Suppliers.Add(Supplier);
                db.SaveChanges();
                return RedirectToPage("/suppliers");
            }
            else
            {
                return Page(); // return to original page
            }
        }

        public void OnGet()
        {
            ViewData["Title"] = "Northwind B2B - Suppliers";

            Suppliers = db.Suppliers.OrderBy(c => c.Country).ThenBy(c => c.CompanyName);
        }
    }
}
