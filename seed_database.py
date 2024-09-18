import requests
from toolz import pipe
from toolz.curried import partial
import repository.database as db

def fetch_trivia_questions():
    url = 'https://opentdb.com/api.php?amount=20'
    response = requests.get(url)
    questions = response.json()['results']

    def add_question_to_db(q):
        with db.get_db_connection() as connection, connection.cursor() as cursor:
            cursor.execute('''
                INSERT INTO questions (question_text, correct_answer)
                VALUES (%s, %s)''', (q['question'], q['correct_answer']))

    pipe(
        questions,
        partial(map, add_question_to_db),
        list
    )

def fetch_users():
    url = 'https://randomuser.me/api?results=4'
    response = requests.get(url)
    data = response.json()['results']

    def add_user_to_db(user):
        with db.get_db_connection() as connection, connection.cursor() as cursor:
            cursor.execute('''
                INSERT INTO users (first, last, email)
                VALUES (%s, %s, %s)''', (user['name']['first'], user['name']['last'], user['email']))

    pipe(
        data,
        partial(map, add_user_to_db),
        list
    )


