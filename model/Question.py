from dataclasses import dataclass

@dataclass
class Question:
   question_text: str
   correct_answer: str
   id: int = None

   @classmethod
   def from_dict(cls, data: dict):
      return cls(
         question_text=data.get('question_text'),
         correct_answer=data.get('correct_answer')
      )