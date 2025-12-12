"""Password generator GUI application."""

import json
import tkinter as tk
from random import choice, randint, shuffle
from tkinter import messagebox

from pandas.io import clipboard
from passwords_utils import letters, numbers, symbols

# Constants
LOGO_PATH = "./days_of_code/gui/img/lock.png"
DEFAULT_EMAIL = "username@email.com"
PASSWORD_FILE = "./days_of_code/gui/data/passwords.json"


def gen_secure_password():
    """Generate a secure password."""
    password_list = [choice(letters) for _ in range(randint(8, 10))]
    password_list.extend([choice(symbols) for _ in range(randint(2, 4))])
    password_list.extend([choice(numbers) for _ in range(randint(2, 4))])

    shuffle(password_list)

    password = "".join(password_list)
    password_input.delete(0, "end")  # Delete any text currently present
    password_input.insert(tk.END, string=password)
    clipboard.copy(password)  # Make accessible to website


def find_password():
    """Search to see if the website has a previously saved username and password."""
    website = website_input.get()
    try:
        # If the file exists, update the data
        with open(PASSWORD_FILE) as f:
            data = json.load(f)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found")
    else:  # Execute if no exception is caught
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(
                title=website,
                message=f"Username: {email}\nPassword: {password}",
            )
        else:
            messagebox.showinfo(
                title=website, message="No details for the website exists."
            )


def any_empty_fields(website, email, password):
    """Check if any of the fields are empty."""
    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showinfo(
            title="Error",
            message="None of the fields are allowed to be empty.\n"
            "Please enter a website, email, and password.",
        )
        return True


def confirm(website, email, password):
    """Confirm the user wants to enter the information provided."""
    return messagebox.askokcancel(
        title=website,
        message=f"Email: {email}\nPassword: {password}\n\nProceed to saving?",
    )


def clear():
    """Clear all the inputs and reset the focus."""
    website_input.delete(0, "end")
    password_input.delete(0, "end")

    website_input.focus()


def save():
    """Write information entered onto GUI into password file."""
    website = website_input.get()
    email = email_input.get()
    password = password_input.get()

    if not any_empty_fields(website, email, password):
        continue_saving = confirm(website, email, password)
        new_password = {website: {"email": email, "password": password}}

        if continue_saving:
            try:
                # If the file exists, update the data
                with open(PASSWORD_FILE) as f:
                    data = json.load(f)
                    data.update(new_password)
            except FileNotFoundError:
                # If the file does not exist, prepare to write only the new password
                data = new_password
            finally:
                # Write the data and clean up the GUI
                with open(PASSWORD_FILE, "w") as f:
                    json.dump(data, f, indent=4)

                clear()


if __name__ == "__main__":
    """Set up the UI."""
    window = tk.Tk()
    window.title("Password Manager")
    window.config(padx=50, pady=50)

    canvas = tk.Canvas(width=200, height=200, highlightthickness=0)
    img = tk.PhotoImage(file=LOGO_PATH)
    canvas.create_image(100, 100, image=img)
    canvas.grid(column=1, row=0)

    website_label = tk.Label(text="Website:")
    website_label.grid(column=0, row=1, padx=3)

    email_label = tk.Label(text="Email/Username:")
    email_label.grid(column=0, row=2, padx=3)

    password_label = tk.Label(text="Password:")
    password_label.grid(column=0, row=3, padx=3)

    website_input = tk.Entry(width=32)
    website_input.grid(column=1, row=1, sticky="w")
    website_input.focus()

    email_input = tk.Entry(width=51)
    email_input.grid(column=1, row=2, columnspan=2, sticky="w")
    email_input.insert(tk.END, DEFAULT_EMAIL)

    password_input = tk.Entry(width=32)
    password_input.grid(column=1, row=3, sticky="w")

    search_btn = tk.Button(text="Search", command=find_password, width=14)
    search_btn.grid(column=2, row=1, sticky="w")

    password_btn = tk.Button(
        text="Generate Password", command=gen_secure_password
    )
    password_btn.grid(column=2, row=3, sticky="w")

    add_btn = tk.Button(text="Add", command=save)
    add_btn.grid(column=1, row=4, columnspan=2, sticky="ew")

    window.mainloop()
