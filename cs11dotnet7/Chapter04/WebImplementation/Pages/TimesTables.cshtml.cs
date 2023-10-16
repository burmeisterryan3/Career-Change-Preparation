using Microsoft.AspNetCore.Mvc; // IActionResult
using Microsoft.AspNetCore.Mvc.RazorPages; // PageModel

namespace WebImplementation.Pages;

public class TimesTablesModel : PageModel
{
    public int number;
    public int size;

    public TimesTablesModel()
    {
        number = 1;
        size = 10;
    }

    public void OnGet()
    {
        ViewData["Title"] = "Times Tables";
    }
        public IActionResult OnPost()
    {
        number = int.Parse(Request.Form["number"]!)!;
        size = int.Parse(Request.Form["size"]!)!;

        ViewData["Result"] = TimesTable(number, size);

        return Page();
    }
    static string TimesTable(int number, int size=10)
    {
        string output = "";
        output += $"This is the {number} times table with {size} rows:\n";
        for (int row = 1; row <= size; row++)
        {
            output += $"{row} x {number} = {row * number}\n";
        }

        return output;
    }
}
