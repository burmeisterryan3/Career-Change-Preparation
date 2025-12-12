"""Create a miles to kilometer widget."""

import tkinter as tk
from functools import partial

CONVERSION_FACTOR = 1.609344
FONT_SIZE = 15
FONT = "Arial"
PADDING = 10


def convert(entry, label):
    """Convert value in the entry field from miles to kilometers."""
    try:
        kilometers = round(int(entry.get()) * CONVERSION_FACTOR)
    except ValueError:
        print("Invalid input. Entry must be a number.")

    label.config(text=f"{kilometers}")


if __name__ == "__main__":
    window = tk.Tk()
    window.title("Miles to Kilometers Converter")
    window.minsize(width=200, height=100)
    window.config(padx=20, pady=20)

    entry = tk.Entry(width=10, font=(FONT, FONT_SIZE))
    entry.insert(tk.END, string="0")
    entry.grid(column=1, row=0, padx=10, pady=10)

    label = tk.Label(text="Miles", font=(FONT, FONT_SIZE))
    label.grid(column=2, row=0, padx=PADDING, pady=PADDING, sticky="w")

    label = tk.Label(text="is equal to", font=(FONT, FONT_SIZE))
    label.grid(column=0, row=1, padx=PADDING, pady=PADDING)

    label_km = tk.Label(text="0", font=(FONT, FONT_SIZE))
    label_km.grid(column=1, row=1, padx=PADDING, pady=PADDING)

    label = tk.Label(text="Kilometers", font=(FONT, FONT_SIZE))
    label.grid(column=2, row=1, padx=PADDING, pady=PADDING)

    button = tk.Button(
        text="Calculate",
        command=partial(convert, entry, label_km),
        font=(FONT, FONT_SIZE),
    )
    button.grid(column=1, row=2)
    button.config(padx=PADDING, pady=PADDING)

    window.mainloop()
