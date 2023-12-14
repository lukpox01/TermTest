from dataclasses import dataclass


@dataclass
class Question:
    question: str
    correct: int | str
    done: bool
    type: int

    def __eq__(self, other):
        return self.type == other.type


@dataclass
class OptionsQuestion(Question):
    options: list[str]


@dataclass
class EntryQuestion(Question):
    placeholder: str


@dataclass
class Test:
    autor: str
    filename: str
    title: str
    description: str
    questions: list[OptionsQuestion | EntryQuestion]
    time_to_complete: int  # minutes

    def __str__(self):
        return f"{self.autor}: {self.title}: {self.questions}"
