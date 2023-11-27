def get_num_cookies():
    """Get the number of cookies to bake."""
    num_cookies = input("How many cookies would you like? ")
    try:
        num_cookies = int(num_cookies)
        return num_cookies
    except ValueError:
        print("That's not a number! Try again.")
        get_num_cookies()

def get_num_people():
    """Get the number of people attending the party."""
    num_people = input("How many people are attending? ")
    try:
        num_people = int(num_people)
        return num_people
    except ValueError as ve:
        print("That's not a number! Try again.")
        print("ValueError:", ve)
        get_num_people()

def divide_cookies(num_cookies, num_people):
    """Divide cookies evenly among people, and print the results."""
    try:
        cookies_per_person = num_cookies // num_people
        leftover_cookies = num_cookies % num_people
        print("Each person get", cookies_per_person,
              "cookies" if cookies_per_person > 1 else "cookie",
              "with", leftover_cookies, "cookies leftover.")
    except ZeroDivisionError as zde:
        print("You can't have a party with no people!")
        print("ZeroDivisionError:", zde)
        divide_cookies(num_cookies, get_num_people())

while True:
    cookies = get_num_cookies()
    people = get_num_people()

    if people > cookies:
        print("You can't have more people than cookies!")
        continue

    divide_cookies(cookies, people)

    if input("Would you like to bake more cookies? (y/n) ") != "y":
        break
