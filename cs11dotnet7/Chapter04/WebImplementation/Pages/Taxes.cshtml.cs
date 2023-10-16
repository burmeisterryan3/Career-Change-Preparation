using Microsoft.AspNetCore.Mvc; // IActionResult
using Microsoft.AspNetCore.Mvc.RazorPages; // PageModel
 
namespace WebImplementation.Pages;

public class TaxesModel : PageModel
{
    public decimal amount;
    public string twoLetterRegionCode;

    public TaxesModel()
    {
        amount = 0;
        twoLetterRegionCode = "VA";
    }

    public void OnGet()
    {
        ViewData["Title"] = "Taxes";
    }

    public IActionResult OnPost()
    {
        amount = decimal.Parse(Request.Form["amount"]!)!;
        string twoLetterRegionCode = Request.Form["twoLetterRegionCode"]!;

        decimal taxToPay = CalculateTax(amount, twoLetterRegionCode);

        ViewData["Result"] = $"For {amount:C} in {twoLetterRegionCode} tax is {taxToPay:C}. Your total is {amount + taxToPay:C}.";

        return Page();
    }

    static decimal CalculateTax(decimal amount, string twoLetterRegionCode)
    {
        decimal rate;
        rate = twoLetterRegionCode switch
        {
            "CH" => 0.08M, // Switzerland
            "DK" or "NO" => 0.25M, // Denmark or Norway
            "GB" or "FR" => 0.2M, // United Kingdom or France
            "HU" => 0.27M, // Hungary
            "OR" or "AK" or "MT" => 0.0M, // Oregon, Alaska, or Montana
            "ND" or "WI" or "ME" or "VA" => 0.05M, // North Dakota, Wisconsin, Maine, or Virginia
            "CA" => 0.0825M, // California
            _ => 0.06M // most US states
        };
        return amount * rate;
    }
}
