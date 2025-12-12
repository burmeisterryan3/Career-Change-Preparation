"""Introduction to GUIs, *args, and **kwargs."""

import tkinter
from functools import partial


def button_clicked(label, entry):
    """Action to take when a button is clicked."""
    label.config(text=entry.get())


if __name__ == "__main__":
    window = tkinter.Tk()
    window.title("Hello, World!")
    window.minsize(width=500, height=300)
    window.config(padx=20, pady=20)

    my_label = tkinter.Label(text="I am a label.", font=("Arial", 14, "bold"))
    my_label.grid(column=0, row=0)
    my_label.config(padx=40, pady=40)

    my_input = tkinter.Entry(width=10)
    my_input.grid(column=3, row=2)

    my_button = tkinter.Button(
        text="Click Me",
        command=partial(button_clicked, my_label, my_input),
    )
    my_button.grid(column=1, row=1)

    my_second_button = tkinter.Button(
        text="Second Button",
        command=partial(button_clicked, my_label, my_input),
    )
    my_second_button.grid(column=2, row=0)

    window.mainloop()
