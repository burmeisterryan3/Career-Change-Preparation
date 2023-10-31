int max = 500;
checked
{
    try
    {
        for (byte i = 0; i < max; i++)
        {
            WriteLine(i);
        }
    }
    catch (OverflowException ex) 
    { 
        WriteLine($"{ex.GetType()}: {ex.Message}");
    }
}
