from typing import List

from model.UserAnswer import UserAnswer
from repository.database import get_db_connection


def create_user_answer(answer: UserAnswer) -> int:
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO user_answers (user_id, question_id, answer_text, is_correct, time_taken)
            VALUES (%s, %s, %s, %s, %s) RETURNING id
        """, (answer.user_id, answer.question_id, answer.answer_text, answer.is_correct, answer.time_taken))
        new_id = cursor.fetchone()['id']
        connection.commit()
        return new_id

def get_user_answers() -> List[UserAnswer]:
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("SELECT * FROM user_answers")
        answers = cursor.fetchall()
        return [UserAnswer(**answer) for answer in answers]

def get_answers_by_user_id(user_id: int) -> List[UserAnswer]:
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("SELECT * FROM user_answers WHERE user_id = %s", (user_id,))
        answers = cursor.fetchall()
        return [UserAnswer(**answer) for answer in answers]

def get_answers_by_question_id(question_id: int) -> List[UserAnswer]:
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("SELECT * FROM user_answers WHERE question_id = %s", (question_id,))
        answers = cursor.fetchall()
        return [UserAnswer(**answer) for answer in answers]

def delete_answer(answer_id: int):
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute('DELETE FROM users WHERE id = %s', (answer_id,))
        connection.commit()

def update_user_answer(answer: UserAnswer, answer_id: int):
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("""
                    UPDATE users SET answer_text = %s, is_correct = %s, time_taken = %s
                    WHERE id = %s;
                """, (answer.answer_text, answer.is_correct, answer.time_taken, answer_id))
        connection.commit()