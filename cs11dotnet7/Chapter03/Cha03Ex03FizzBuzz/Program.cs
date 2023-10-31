for (int i=1; i<=100; i++)
{
    if (IsDivByFifteen(i))
    {
        Write("FizzBuzz");
    }
    else if (IsDivByFive(i))
    {
        Write("Buzz");
    }
    else if (IsDivByThree(i))
    {
        Write("Fizz");
    }
    else
    {
        Write($"{i}");
    }

    if (i != 100) { Write(", "); }
    if (i % 10 == 0) { WriteLine(); }
}

static bool IsDivByThree(int a)
{
    return a % 3 == 0;
}

static bool IsDivByFive(int a)
{
    return a % 5 == 0;
}

static bool IsDivByFifteen(int a)
{
    return a % 15 == 0;
}
