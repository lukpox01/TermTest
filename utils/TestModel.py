from dataclasses import dataclass


@dataclass
class Question:
    question: str
    options: list[str]
    correct: int
    done: bool


@dataclass
class Test:
    autor: str
    filename: str
    title: str
    description: str
    questions: list[Question]
    time_to_complete: int  # minutes

    def __str__(self):
        return f"{self.autor}: {self.title}: {self.questions}"
