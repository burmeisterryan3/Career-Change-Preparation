##########################################################################
# Quiz 1: Scripting with Raw Input
##########################################################################

#### Question 1:
"""
Imagine you're a teacher who needs to send a message to each of your students reminding them of their missing assignments and grade in the class. You have each of their names, number of missing assignments, and grades on a spreadsheet and just have to insert them into placeholders in this message you came up with:

Hi [insert student name],
This is a reminder that you have [insert number of missing assignments] assignments left to submit before you can graduate. Your current grade is [insert current grade] and can increase to [insert potential grade] if you submit all assignments before the due date.

You can just copy and paste this message to each student and manually insert the appropriate values each time, but instead you're going to write a program that does this for you.

Write a script that does the following:
1. Ask for user input 3 times. Once for a list of names, once for a list of missing assignment counts, and once for a list of grades. Use this input to create lists for names, assignments, and grades.
2. Use a loop to print the message for each student with the correct values. The potential grade is simply the current grade added to two times the number of missing assignments.
"""
names = input('Enter names separated by commas: ').split(',')
assignments =  input('Enter assignment counts separated by commas: ').split(',')
grades =  input('Enter grades separated by commas: ').split(',')
print ("\n")

message = message = "Hi {},\n\nThis is a reminder that you have {} assignments left to \
submit before you can graduate. You're current grade is {} and can increase \
to {} if you submit all assignments before the due date.\n\n"
# write a for loop that iterates through each set of names, assignments, and grades to print each student's message
for name, num_assignments, grade in zip(names, assignments, grades):
    print(message.format(name.title(), num_assignments, grade, int(grade) + 2*int(num_assignments)))

"""
Try Statement
We can use try statements to handle exceptions. There are four clauses you can use (one more in addition to those shown in the video).

try: This is the only mandatory clause in a try statement. The code in this block is the first thing that Python runs in a try statemen
except: If Python runs into an exception while running the try block, it will jump to the except block that handles that exception.
else: If Python runs into no exceptions while running the try block, it will run the code in this block after running the try block.
finally: Before Python leaves this try statement, it will run the code in this finally block under any conditions, even if it's ending the program. E.g., if Python ran into an error while running code in the except or else block, this finally block will still be executed before stopping the program.
"""

def party_planner(cookies, people):
    leftovers = None
    num_each = None
    try:
        num_each = cookies // people
        leftovers = cookies % people
    except ZeroDivisionError:
        print('The number of people attending must be greater than 0.')

    return(num_each, leftovers)

# The main code block is below; do not edit this
lets_party = 'y'
while lets_party == 'y':

    cookies = int(input("How many cookies are you baking? "))
    people = int(input("How many people are attending? "))

    cookies_each, leftovers = party_planner(cookies, people)

    if cookies_each:  # if cookies_each is not None
        message = "\nLet's party! We'll have {} people attending, they'll each get to eat {} cookies, and we'll have {} left over."
        print(message.format(people, cookies_each, leftovers))

    lets_party = input("\nWould you like to party more? (y or n) ")

# Accessing error message -
try:
    # some code
except ZeroDivisionError as e:
   # some code
   print("ZeroDivisionError occurred: {}".format(e))

##########################################################################
# Quiz 2: Reading and Writing Files
##########################################################################

#### Question 1:
# Use the relevant part of the Python documentation to find a method that reads the next line of a file. Put the name of the method in the box.
camelot_lines = []
with open("camelot.txt") as f:
    for line in f:
        camelot_lines.append(line.strip())

print(camelot_lines)

#### Question 2:
# You're going to create a list of the actors who appeared in the television programme Monty Python's Flying Circus.
# Write a function called create_cast_list that takes a filename as input and returns a list of actors' names. It will be run on the file flying_circus_cast.txt (this information was collected from imdb.com). Each line of that file consists of an actor's name, a comma, and then some (messy) information about roles they played in the programme. You'll need to extract only the name and add it to a list. You might use the .split() method to process each line.
def create_cast_list(filename):
    cast_list = []
    with open(filename) as f:
        for line in f:
            cast_list.append(line.split(',')[0])

    return cast_list

cast_list = create_cast_list('flying_circus_cast.txt')
for actor in cast_list:
    print(actor)

    # initiate empty list to hold user input and sum value of zero
user_list = []
list_sum = 0

# seek user input for ten numbers 
for i in range(10):
    
##########################################################################
# Quiz 3: Practice Debugging
##########################################################################    
# check to see if number is even and if yes, add to list_sum
# print incorrect value warning  when ValueError exception occurs
    try:
        number = int(input("Enter any 2-digit number: "))
        user_list.append(number)
        if number % 2 == 0:
            list_sum += number
    except ValueError:
        print("Incorrect value. That's not an int!")

print("user_list: {}".format(user_list))
print("The sum of the even numbers in user_list is: {}.".format(list_sum))

"""
Main

# useful_functions.py

def mean(num_list):
    return sum(num_list) / len(num_list)

def add_five(num_list):
    return [n + 5 for n in num_list]

def main():
    print("Testing mean function")
    n_list = [34, 44, 23, 46, 12, 24]
    correct_mean = 30.5
    assert(mean(n_list) == correct_mean)

    print("Testing add_five function")
    correct_list = [39, 49, 28, 51, 17, 29]
    assert(add_five(n_list) == correct_list)

    print("All tests passed!")

if __name__ == '__main__':
    main()
"""

##########################################################################
# Quiz 4: The Standard Library
##########################################################################

#### Question 1:
# print e to the power of 3 using the math module
import math
print(math.exp(3))

#### Question 2:
# Write a function called generate_password that selects three random words from the list of words word_list and concatenates them into a single string. Your function should not accept any arguments and should reference the global variable word_list to build the password.
# TODO: First rt the `random` module
import random

# We begin with an empty `word_list`
word_file = "words.txt"
word_list = []

# We fill up the word_list from the `words.txt` file
with open(word_file,'r') as words:
	for line in words:
		# remove white space and make everything lowercase
		word = line.strip().lower()
		# don't include words that are too long or too short
		if 3 < len(word) < 8:
			word_list.append(word)

# TODO: Add your function generate_password below
# It should return a string consisting of three random words 
# concatenated together without space
def generate_password():
    return ''.join(random.choices(word_list, k=3)) # with replacement

# Now we test the function
print(generate_password())

"""
Useful Modules -

csv: very convenient for reading and writing csv files
collections: useful extensions of the usual data types including OrderedDict, defaultdict and namedtuple
random: generates pseudo-random numbers, shuffles sequences randomly and chooses random items
string: more functions on strings. This module also contains useful collections of letters like string.digits (a string containing all characters which are valid digits).
re: pattern-matching in strings via regular expressions
math: some standard mathematical functions
os: interacting with operating systems
os.path: submodule of os for manipulating path names
sys: work directly with the Python interpreter
json: good for reading and writing json files (good for web work)
"""

"""
requirements.txt

Larger Python programs might depend on dozens of third party packages. To make it easier to share these programs, programmers often list a project's dependencies in a file called requirements.txt. This is an example of a requirements.txt file.

beautifulsoup4==4.5.1
bs4==0.0.1
pytz==2016.7
requests==2.11.1

Each line of the file includes the name of a package and its version number. The version number is optional, but it usually should be included. Libraries can change subtly, or dramatically, between versions, so it's important to use the same library versions that the program's author used when they wrote the program.

You can use pip to install all of a project's dependencies at once by typing "pip install -r requirements.txt" in your command line.
"""

##########################################################################
# Practice Question
##########################################################################

# Create a function that opens the flowers.txt, reads every line in it, and saves it as a dictionary. The main (separate) function should take user input (user's first name and last name) and parse the user input to identify the first letter of the first name. It should then use it to print the flower name with the same first letter (from dictionary created in the first function).
# Write your code here

# HINT: create a dictionary from flowers.txt
def create_dict(filename):
    flower_dict = dict()
    with open(filename) as f:
        for line in f:
            letter, flower = line.split(": ")
            # letter, flower = line.split(":")
            # flower = flower.lstrip()
            flower_dict[letter] = flower.strip()
    return flower_dict

# HINT: create a function to ask for user's first and last name
def request_username():
    return input("Enter your First [space] Last name only: ")
    
# print the desired output
def main():
    fname = "flowers.txt"
    username = request_username()
    flower_dict = create_dict(fname)
    print("Unique flower name with the first letter: {}".format(flower_dict[username[0]]))

if __name__ == '__main__':
    main()