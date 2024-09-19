from typing import List

from model.Question import Question
from repository.database import get_db_connection

def get_all_questions() -> List[Question]:
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute('SELECT * FROM questions')
        questions = cursor.fetchall()
        return [Question(**q) for q in questions]

def get_by_id(question_id: int) -> Question:
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute('SELECT * FROM questions WHERE id = %s', (question_id,))
        res = cursor.fetchone()
        question = Question(**res)
        connection.commit()
        return question

def delete_question(question_id: int):
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute('DELETE FROM questions WHERE id = %s', (question_id,))
        connection.commit()

def create_question(question: Question) -> int:
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO questions (question_text, correct_answer)
            VALUES (%s, %s) RETURNING id
        """, (question.question_text, question.correct_answer))
        new_id = cursor.fetchone()['id']
        connection.commit()
        return new_id

def update_question(question: Question, question_id: int):
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("""
                    UPDATE questions SET question_text = %s, correct_answer = %s
                    WHERE id = %s;
                """, (question.question_text, question.correct_answer, question_id))
        connection.commit()
