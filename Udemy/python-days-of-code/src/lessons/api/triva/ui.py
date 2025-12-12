import tkinter as tk
from functools import partial
from pathlib import Path

from quiz_brain import QuizBrain

THEME_COLOR = "#375362"
IMG_PATH = Path("./images/")
PADDING = 20
QUOTE_WIDTH = 250
QUOTE_HEIGHT = 300
QUOTE_FONT = ("Arial", 20, "italic")


class QuizInterface:
    def __init__(self, quiz_brain: QuizBrain):
        self.quiz = quiz_brain

        self.window = tk.Tk()
        self.window.title("Quizzler")
        self.window.config(padx=PADDING, pady=PADDING, bg=THEME_COLOR)

        self.score_label = tk.Label(
            text="Score: 0", fg="white", bg=THEME_COLOR
        )
        self.score_label.grid(row=0, column=1)

        self.canvas = tk.Canvas(
            width=QUOTE_WIDTH, height=QUOTE_HEIGHT, bg="white"
        )

        self.question_text = self.canvas.create_text(
            QUOTE_WIDTH / 2,
            QUOTE_HEIGHT / 2,
            text="TEST",
            width=QUOTE_WIDTH - 20,
            fill=THEME_COLOR,
            font=QUOTE_FONT,
        )
        self.canvas.grid(row=1, column=0, columnspan=2, pady=50)

        false_image = tk.PhotoImage(file=IMG_PATH / "false.png")
        self.false_btn = tk.Button(
            image=false_image,
            highlightthickness=0,
            bg=THEME_COLOR,
            command=partial(self.check_answer, "False"),
        )
        self.false_btn.grid(row=2, column=1)

        true_image = tk.PhotoImage(file=IMG_PATH / "true.png")
        self.true_btn = tk.Button(
            image=true_image,
            highlightthickness=0,
            bg=THEME_COLOR,
            command=partial(self.check_answer, "True"),
        )
        self.true_btn.grid(row=2, column=0)

        self.gen_next_question()

        self.window.mainloop()

    def gen_next_question(self) -> None:
        self.canvas.config(bg="white")
        if self.quiz.still_has_questions():
            q_text = self.quiz.next_question()
            self.canvas.itemconfig(self.question_text, text=q_text)
        else:
            q_text = (
                "You've completed the quiz!\n\n"
                + f"Your final score was: {self.quiz.score}/{self.quiz.question_number}"
            )
            self.canvas.itemconfig(self.question_text, text=q_text)
            self.true_btn.config(state="disabled")
            self.false_btn.config(state="disabled")

    def update_score(self) -> None:
        self.score_label.config(text=f"Score: {self.quiz.score}")

    def check_answer(self, answer: str) -> None:
        self.give_feedback(self.quiz.check_answer(answer))
        self.update_score()

    def give_feedback(self, is_right: bool):
        if is_right:
            self.canvas.config(bg="green")
        else:
            self.canvas.config(bg="red")
        self.canvas.after(500, self.gen_next_question)
