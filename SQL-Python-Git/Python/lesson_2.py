#                    MUTABLE
#                       |
#                       | 
#              Sets     |     Lists
#       Dictonaries     |
#                       |
# UNORDERED ----------- | ----------- ORDERED
#                       |
#                       |    Strings
#                       |    Tuples
#                       | 
#                       |
#                   IMMUTABLE

# Tuples - A tuple is an immutable, ordered data structure that can be indexed and sliced like a list. Tuples are defined by listing a sequence of elements separated by commas, optionally contained within parentheses: ().
# Sets - A set is a mutable data structure - you can modify the elements in a set with methods like add and pop. A set is an unordered data structure, so you can't index and slice elements like a list; there is no sequence of positions to index with!
# Dictionaries - A dictionary is a mutable, unordered data structure that contains mappings of keys to values. Because these keys are used to index values, they must be unique and immutable. For example, a string or tuple can be used as the key of a dictionary, but if you try to use a list as a key of a dictionary, you will get an error.

#
#   Data Structure  Ordered     Mutable     Constructor	        Example
#   List	        Yes	        Yes	        [ ] or list()	    [5.7, 4, 'yes', 5.7]
#   Tuple	        Yes	        No	        ( ) or tuple()	    (5.7, 4, 'yes', 5.7)
#   Set	            No	        Yes	        {}* or set()	    {5.7, 4, 'yes'}
#   Dictionary	    No	        No**	    { } or dict()	    {'Jun': 75, 'Jul': 89}

# * You can use curly braces to define a set like this: {1, 2, 3}. However, if you leave the curly braces empty like this: {} Python will instead create an empty dictionary. So to create an empty set, use set().
# ** A dictionary itself is mutable, but each of its individual keys must be immutable.

##########################################################################
# Quiz 1: List Indexing
##########################################################################

# Use list indexing to determine how many days are in a particular month based on the integer variable month, and store that value in the integer variable num_days. For example, if month is 8, num_days should be set to 31, since the eighth month, August, has 31 days.

month = 8
days_in_month = [31,28,31,30,31,30,31,31,30,31,30,31]

# use list indexing to determine the number of days in month
num_days = sum([days for days in days_in_month])

print(num_days)

# Select the three most recent dates from this list using list slicing notation. Hint: negative indexes work in slices!
eclipse_dates = ['June 21, 2001', 'December 4, 2002', 'November 23, 2003',
                 'March 29, 2006', 'August 1, 2008', 'July 22, 2009',
                 'July 11, 2010', 'November 13, 2012', 'March 20, 2015',
                 'March 9, 2016']
                 
                 
# TODO: Modify this line so it prints the last three elements of the list
print(eclipse_dates[-3:])

##########################################################################
# Quiz 2: Dictonaries and Identity Functions
##########################################################################
# Define a Dictionary, population,
# that provides information
# on the world's largest cities.
# The key is the name of a city
# (a string), and the associated
# value is its population in
# millions of people.

#   Key     |   Value
# Shanghai  |   17.8
# Istanbul  |   13.3
# Karachi   |   13.0
# Mumbai    |   12.5

population = {'Shanghai': 17.8, 'Istanbul': 13.3, 'Karachi': 13.0, 'Mumbai': 12.5}

# What will the output of the following code be? (Treat the commas in the multiple choice answers as newlines.)

a = [1, 2, 3]
b = a
c = [1, 2, 3]

print(a == b) # True
print(a is b) # True
print(a == c) # True
print(a is c) # False

# That's correct! List a and list b are equal and identical. List c is equal to a (and b for that matter) since they have the same contents. But a and c (and b for that matter, again) point to two different objects, i.e., they aren't identical objects. That is the difference between checking for equality vs. identity.

##########################################################################
# Quiz 3: Data Structures
##########################################################################

# invalid dictionary - this should break - Mutable data type for key
room_numbers = {
    ['Freddie', 'Jen']: 403,
    ['Ned', 'Keith']: 391,
    ['Kristin', 'Jazzmyne']: 411,
    ['Eugene', 'Zach']: 395
}

# Does not break - immutable type (set) for key
room_numbers = {
    ('Freddie', 'Jen'): 403,
    ('Ned', 'Keith'): 391,
    ('Kristin', 'Jazzmyne'): 411,
    ('Eugene', 'Zach'): 395
}

##########################################################################
# Quiz 4: Compound Data Structures
##########################################################################

# Try your hand at working with nested dictionaries. Add another entry, 'is_noble_gas,' to each dictionary in the elements dictionary. After inserting the new entries you should be able to perform these lookups:

elements = {'hydrogen': {'number': 1, 'weight': 1.00794, 'symbol': 'H'},
            'helium': {'number': 2, 'weight': 4.002602, 'symbol': 'He'}}

# todo: Add an 'is_noble_gas' entry to the hydrogen and helium dictionaries
# hint: helium is a noble gas, hydrogen isn't
elements['hydrogen']['is_noble_gas'] = False
elements['helium']['is_noble_gas'] = True

##########################################################################
# Quiz 5: Practice Questions
##########################################################################

# Your task for this quiz is to find the number of unique words in the text. In the code editor below, complete these three steps to get your answer.

# 1. Split verse into a list of words. Hint: You can use a string method you learned in the previous lesson.
# 2. Convert the list into a data structure that would keep only the unique elements from the list.
# 3. Print the length of the container.

verse = "if you can keep your head when all about you are losing theirs and blaming it on you   if you can trust yourself when all men doubt you     but make allowance for their doubting too   if you can wait and not be tired by waiting      or being lied about  don’t deal in lies   or being hated  don’t give way to hating      and yet don’t look too good  nor talk too wise"
print(verse, '\n')

# split verse into list of words
verse_list = verse.split()
print(verse_list, '\n')

# convert list to a data structure that stores unique elements
verse_set = set(verse_list)
print(verse_set, '\n')

# print the number of unique words
num_unique = len(verse_set)
print(num_unique, '\n')

# In the code editor below, you'll find a dictionary containing the unique words of verse stored as keys and the number of times they appear in verse stored as values. Use this dictionary to answer the following questions. Submit these answers in the quiz below the code editor.

# 1. How many unique words are in verse_dict?
# 2. Is the key "breathe" in verse_dict?
# 3. What is the first element in the list created when verse_dict is sorted by keys?
#    Hint: Use the appropriate dictionary method to get a list of its keys, and then sort that list. Use this list of keys to answer the next two questions as well.
# 4. Which key (word) has the highest value in verse_dict?

verse_dict =  {'if': 3, 'you': 6, 'can': 3, 'keep': 1, 'your': 1, 'head': 1, 'when': 2, 'all': 2, 'about': 2, 'are': 1, 'losing': 1, 'theirs': 1, 'and': 3, 'blaming': 1, 'it': 1, 'on': 1, 'trust': 1, 'yourself': 1, 'men': 1, 'doubt': 1, 'but': 1, 'make': 1, 'allowance': 1, 'for': 1, 'their': 1, 'doubting': 1, 'too': 3, 'wait': 1, 'not': 1, 'be': 1, 'tired': 1, 'by': 1, 'waiting': 1, 'or': 2, 'being': 2, 'lied': 1, 'don\'t': 3, 'deal': 1, 'in': 1, 'lies': 1, 'hated': 1, 'give': 1, 'way': 1, 'to': 1, 'hating': 1, 'yet': 1, 'look': 1, 'good': 1, 'nor': 1, 'talk': 1, 'wise': 1}
print(verse_dict, '\n')

# find number of unique keys in the dictionary
num_keys = len(verse_dict)
print(num_keys)

# find whether 'breathe' is a key in the dictionary
contains_breathe = verse_dict.get('breathe') # "breathe" in verse_dict
print(contains_breathe)

# create and sort a list of the dictionary's keys
sorted_keys = sorted(list(verse_dict.keys()))

# get the first element in the sorted list of keys
print(sorted_keys[0])

# find the element with the highest value in the list of keys
print(sorted_keys[-1]) 