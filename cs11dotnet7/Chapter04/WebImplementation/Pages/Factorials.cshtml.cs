using Microsoft.AspNetCore.Mvc; // IActionResult
using Microsoft.AspNetCore.Mvc.RazorPages; // PageModel

namespace WebImplementation.Pages;

public class FactorialsModel : PageModel
{
    public int number;

    public FactorialsModel()
    {
        number = 0;
    }

    public void OnGet()
    {
        ViewData["Title"] = "Factorials";
    }

    public IActionResult OnPost()
    {
        number = int.Parse(Request.Form["number"]!)!;
        int result = Factorial(number);

        ViewData["Result"] = $"The factorial of {number} is {result}.";

        return Page();
    }

    static int Factorial(int number)
    {
        if (number < 0)
        {
            throw new ArgumentException(
                message: "The factorial function is defined for " +
                         $"non-negative integers only. Input: {number}",
                paramName: nameof(number));
        }
        else if (number == 0)
        {
            return 1;
        }
        else
        {
            checked // for overflow, int overflows for numbers >= 13
            {
                return number * Factorial(number - 1);
            }
        }
    }
}
