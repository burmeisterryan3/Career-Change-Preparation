using CallStackExceptionHandlingLib;

WriteLine("In Main");
Alpha();
void Alpha()
{
    WriteLine("In Alpha");
    Beta();
}
void Beta()
{
    WriteLine("In Beta");
    try
    {
        Calculator.Gamma();
    }
    catch (Exception ex)
    {
        WriteLine($"Caught this: {ex.Message}");
        // Below is worse option than just "throw" as it loses some call stack information
        // throw ex
        throw;
    }
}
