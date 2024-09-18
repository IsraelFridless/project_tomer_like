from typing import List

from model.Answer import Answer
from repository.database import get_db_connection

def get_by_id(answer_id: int) -> List[Answer]:
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute('SELECT * FROM answers WHERE question_id = %s', (answer_id,))
        res = cursor.fetchall()
        answers = [Answer(**row) for row in res]
        connection.commit()
        return answers

def delete_answer(answer_id: int):
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute('DELETE FROM answers WHERE id = %s', (answer_id,))
        connection.commit()

def create_answer(answer: Answer, question_id: int) -> int:
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO answers (incorrect_answer, question_id)
            VALUES (%s, %s) RETURNING id
        """, (answer.incorrect_answer, question_id))
        new_id = cursor.fetchone()['id']
        connection.commit()
        return new_id

def update_answer(answer: Answer, answer_id: int):
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("""
                    UPDATE answers SET incorrect_answer = %s
                    WHERE id = %s;
                """, (answer.incorrect_answer, answer_id))
        connection.commit()
