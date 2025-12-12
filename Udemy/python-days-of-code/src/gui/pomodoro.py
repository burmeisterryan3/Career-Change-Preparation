"""Pomodoro timer used for productivity."""

import tkinter as tk

# Constants
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 1
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
LOGO_PATH = "./days_of_code/gui/img/tomato.png"

# Global variables
reps = 1
timer = None


def reset_timer():
    """Reset the timer to the initial condition."""
    global reps, timer
    reps = 1
    window.after_cancel(timer)
    header_label.config(text="Timer", fg=GREEN)
    canvas.itemconfig(timer_text, text="00:00")
    mark_labels.config(text="")


def start_timer():
    """Implements the timing mechanism."""
    global reps
    if reps % 2 == 1:
        minutes = WORK_MIN
        header_label.config(text="Work", fg=GREEN)
    elif reps % 8 == 0:
        # After the fourth iteration of work, take a long break
        minutes = LONG_BREAK_MIN
        header_label.config(text="Break", fg=RED)
    else:
        # Take a short break for the first three work iterations
        minutes = SHORT_BREAK_MIN
        header_label.config(text="Break", fg=PINK)

    reps += 1

    count_down(minutes)


def count_down(count):
    """Implements the count down mechanism."""
    global reps, timer
    minutes = count // 60
    seconds = count % 60
    canvas.itemconfig(timer_text, text=f"{minutes:02}:{seconds:02}")
    if count > 0:
        timer = window.after(1000, count_down, count - 1)
    else:
        # Add a check for a completed work round
        if reps % 2 == 0:
            mark_labels.config(text="✔" * (reps // 2))

        # Reset reps
        if reps == 9:
            mark_labels.config(text="")
            reps = 1

        start_timer()


if __name__ == "__main__":
    # Set up the UI

    window = tk.Tk()
    window.title("Pomodoro")
    window.config(padx=100, pady=50, bg=YELLOW)

    canvas = tk.Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
    tomato_img = tk.PhotoImage(file=LOGO_PATH)
    canvas.create_image(100, 112, image=tomato_img)
    timer_text = canvas.create_text(
        100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold")
    )
    canvas.grid(column=1, row=1)

    header_label = tk.Label(
        text="Timer", bg=YELLOW, fg=GREEN, font=(FONT_NAME, 50)
    )
    header_label.grid(column=1, row=0)

    start_btn = tk.Button(
        text="Start", bg="White", highlightthickness=0, command=start_timer
    )
    start_btn.grid(column=0, row=2)

    reset_btn = tk.Button(
        text="Reset", bg="White", highlightthickness=0, command=reset_timer
    )
    reset_btn.grid(column=2, row=2)

    mark_labels = tk.Label(text="", bg=YELLOW, fg=GREEN)
    mark_labels.grid(column=1, row=3)

    window.mainloop()
