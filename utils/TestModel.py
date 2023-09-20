from dataclasses import dataclass


@dataclass
class Question:
    question: str
    options: list[str]
    correct: int


@dataclass
class Test:
    autor: str
    title: str
    questions: list[Question]
    time_to_complete: int  # minutes
