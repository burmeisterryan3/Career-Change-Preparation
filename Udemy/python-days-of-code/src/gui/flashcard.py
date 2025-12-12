"""French-to-English flashcard GUI application."""

import random
import tkinter as tk

import pandas as pd

# Constants
BACKGROUND_COLOR = "#B1DDC6"
IMG_PATH = "./days_of_code/gui/img/"
DATA_FILE = "./days_of_code/gui/data/french_words.csv"
SAVE_FILE = "./days_of_code/gui/data/words_to_learn.csv"
LANGUAGE_FONT = ("Arial", 40, "italic")
WORD_FONT = ("Arial", 60, "bold")

# Globals
translations = dict()
current_card = dict()


def read_data() -> dict:
    """Read the data from the French to English csv file."""
    global translations
    try:
        df = pd.read_csv(SAVE_FILE, delimiter=",", header=0)
    except FileNotFoundError:
        df = pd.read_csv(DATA_FILE, delimiter=",", header=0)

    translations = df.to_dict(orient="records")


def is_known():
    """Update the list of cards that need to be learned given a correct translation."""
    translations.remove(current_card)

    if len(translations) == 0:
        canvas.itemconfig(card_title, text="No more words!", fill="black")
        canvas.itemconfig(card_word, text="You win!", fill="black")
        canvas.itemconfig(card_background, image=card_front)
    else:
        pd.DataFrame(translations).to_csv(SAVE_FILE, index=False)
        next_card()


def next_card():
    """Update the canvass with a new French word."""
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(translations)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(card_background, image=card_front)
    window.after(3000, func=flip_card)


def flip_card():
    """Flip the card to reveal the translation."""
    global current_card
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_background, image=card_back)


if __name__ == "__main__":
    read_data()

    """Set up the UI."""
    window = tk.Tk()
    window.title("Flashy")
    window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

    flip_timer = window.after(3000, func=flip_card)

    canvas = tk.Canvas(width=800, height=526)
    canvas.config(highlightthickness=0, bg=BACKGROUND_COLOR)

    card_front = tk.PhotoImage(file=IMG_PATH + "card_front.png")
    card_back = tk.PhotoImage(file=IMG_PATH + "card_back.png")

    card_background = canvas.create_image(400, 263, image=card_front)
    card_title = canvas.create_text(400, 150, text="", font=LANGUAGE_FONT)
    card_word = canvas.create_text(400, 263, text="", font=WORD_FONT)
    canvas.grid(column=0, row=0, columnspan=2)

    wrong_image = tk.PhotoImage(file=IMG_PATH + "wrong.png")
    wrong_btn = tk.Button(
        image=wrong_image,
        highlightthickness=0,
        bg=BACKGROUND_COLOR,
        command=next_card,
    )
    wrong_btn.grid(column=0, row=1)

    right_image = tk.PhotoImage(file=IMG_PATH + "right.png")
    right_btn = tk.Button(
        image=right_image,
        highlightthickness=0,
        bg=BACKGROUND_COLOR,
        command=is_known,
    )
    right_btn.grid(column=1, row=1)

    next_card()

    window.mainloop()
