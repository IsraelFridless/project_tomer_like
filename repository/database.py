import psycopg2
from psycopg2.extras import RealDictCursor

from config.sql_config import SQLALCHEMY_DATABASE_URI


def get_db_connection():
    return psycopg2.connect(SQLALCHEMY_DATABASE_URI, cursor_factory=RealDictCursor)

def create_tables():
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    first VARCHAR(100) NOT NULL,
                    last VARCHAR(100) NOT NULL,
                    email VARCHAR(100) NOT NULL
                )
                CREATE TABLE IF NOT EXISTS questions (
                    id SERIAL PRIMARY KEY,
                    question_text VARCHAR(255) NOT NULL,
                    correct_answer VARCHAR(255) NOT NULL
                )
                CREATE TABLE IF NOT EXISTS answers (
                    id SERIAL PRIMARY KEY,
                    question_id INTEGER NOT NULL,
                    incorrect_answer VARCHAR(255) NOT NULL,
                    FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE
                )
                CREATE TABLE IF NOT EXISTS user_answers (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    question_id INTEGER NOT NULL,
                    answer_text VARCHAR(255) NOT NULL,
                    is_correct BOOLEAN,
                    time_taken VARCHAR(50) NOT NULL
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                    FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE
                )
                """
            )