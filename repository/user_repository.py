from typing import List

from model.User import User
from repository.database import get_db_connection

def get_all_users() -> List[User]:
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute('SELECT * FROM users')
        users = cursor.fetchall()
        return [User(**u) for u in users]

def get_by_id(user_id: int) -> User:
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
        user = cursor.fetchone()
        return User(**user)

def delete_user(user_id: int):
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute('DELETE FROM users WHERE id = %s', (user_id,))
        connection.commit()

def create_user(user: User) -> int:
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO users (first, last, email)
            VALUES (%s, %s, %s) RETURNING id
        """, (user.first, user.last, user.email))
        new_id = cursor.fetchone()['id']
        connection.commit()
        return new_id

def update_user(user: User, user_id: int):
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("""
                    UPDATE users SET first = %s, last = %s, email = %s
                    WHERE id = %s;
                """, (user.first, user.last, user.email, user_id))
        connection.commit()
