using System.Collections;
using System.Diagnostics.CodeAnalysis;

partial class Program
{
    [StringSyntaxAttribute("Regex")]
    const string digitsOnlyText = @"^\d+$";

    [StringSyntaxAttribute("Regex")]
    const string commaSeparatorText =
        "(?:^|,)(?=[^\"]|(\")?)\"?((?(1)[^\"]*|[^,\"]*))\"?(?=,|$)";
}