from dataclasses import dataclass

@dataclass
class Answer:
   incorrect_answer: str
   question_id: int = None
   id: int = None