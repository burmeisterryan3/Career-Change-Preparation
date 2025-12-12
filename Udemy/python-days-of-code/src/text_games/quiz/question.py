"""Question class."""


class Question:
    """Defines the question class."""

    def __init__(self, text: str, answer: str):  # noqa: D107
        self.text = text
        self.answer = answer
