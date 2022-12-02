##########################################################################
# Quiz 1: Defining Functions
##########################################################################

#### Question 1:
# Write a function named population_density that takes two arguments, population and land_area, and returns a population density calculated from those values. I've included two test cases that you can use to verify that your function works correctly. Once you've written your function, use the Test Run button to test your code.

# write your function here
def population_density(population, land_area):
    return population/land_area

# test cases for your function
test1 = population_density(10, 1)
expected_result1 = 10
print("expected result: {}, actual result: {}".format(expected_result1, test1))

test2 = population_density(864816, 121.4)
expected_result2 = 7123.6902801
print("expected result: {}, actual result: {}".format(expected_result2, test2))

#### Question 2:
# Write a function named readable_timedelta. The function should take one argument, an integer days, and return a string that says how many weeks and days that is. For example, calling the function and printing the result like this:
## print(readable_timedelta(10))
# should output the following:
# 1 week(s) and 3 day(s).

# write your function here
def readable_timedelta(days):
    return('{} week(s) and {} day(s).'.format(days//7, days%7))

# test your function
print(readable_timedelta(10))

##########################################################################
# Quiz 2: Docstrings
##########################################################################

def readable_timedelta(days):
    """Return a string of the number of weeks and days included in days."""
    weeks = days // 7
    remainder = days % 7
    return "{} week(s) and {} day(s)".format(weeks, remainder)
def readable_timedelta(days):
    """Return a string of the number of weeks and days included in days.

    Args:
        days (int): number of days to convert
    """
    weeks = days // 7
    remainder = days % 7
    return "{} week(s) and {} day(s)".format(weeks, remainder)
def readable_timedelta(days):
    """
    Return a string of the number of weeks and days included in days.

    Parameters:
    days -- number of days to convert (int)

    Returns:
    string of the number of weeks and days included in days
    """
    weeks = days // 7
    remainder = days % 7
    return "{} week(s) and {} day(s)".format(weeks, remainder)

##########################################################################
# Quiz 3: Lambda Functions
##########################################################################

"""
You can use lambda expressions to create anonymous functions. That is, functions that don’t have a name. They are helpful for creating quick functions that aren’t needed later in your code. This can be especially useful for higher order functions, or functions that take in other functions as arguments.

With a lambda expression, this function:
"""
def multiply(x, y):
    return x * y

# can be reduced to:
multiply = lambda x, y: x * y

# Both of these functions are used in the same way. In either case, we can call multiply like this:
multiply(4, 7)

#### Question 1:
# map() is a higher-order built-in function that takes a function and iterable as inputs, and returns an iterator that applies the function to each element of the iterable. The code below uses map() to find the mean of each list in numbers to create the list averages. Give it a test run to see what happens.

# Rewrite this code to be more concise by replacing the mean function with a lambda expression defined within the call to map().
numbers = [
              [34, 63, 88, 71, 29],
              [90, 78, 51, 27, 45],
              [63, 37, 85, 46, 22],
              [51, 22, 34, 11, 18]
           ]

# def mean(num_list):
#     return sum(num_list) / len(num_list)

# Option 1:
mean = lambda num_list: sum(num_list)/len(num_list)
averages = list(map(mean, numbers))

# Option 2:
averages = list(map(lambda num_list: sum(num_list) / len(num_list), numbers))
print(averages)

#### Question 2:
# filter() is a higher-order built-in function that takes a function and iterable as inputs and returns an iterator with the elements from the iterable for which the function returns True. The code below uses filter() to get the names in cities that are fewer than 10 characters long to create the list short_cities. Give it a test run to see what happens.

# Rewrite this code to be more concise by replacing the is_short function with a lambda expression defined within the call to filter().
cities = ["New York City", "Los Angeles", "Chicago", "Mountain View", "Denver", "Boston"]

# def is_short(name):
#    return len(name) < 10

# Option 1:
is_short = lambda city: len(city) < 10
short_cities = list(filter(is_short, cities))

# Option 2:
short_cities = list(filter(lambda city: len(city < 10, cities)))
print(short_cities)