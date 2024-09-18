from typing import List, Dict

import requests
from toolz import pipe
from toolz.curried import partial
import repository.database as db
import repository.question_repository as q_repo, repository.answer_repository as ans_repo

import requests
from toolz import pipe
from functools import partial

from model.Answer import Answer
from model.Question import Question

import requests
from toolz import pipe
from functools import partial
from typing import List, Dict

import requests
import time
from typing import List, Dict

# Thank you Gpt
def fetch_trivia_questions():
    url = 'https://opentdb.com/api.php?amount=20'
    max_retries = 3
    retry_delay = 10  # Wait 10 seconds between retries

    for attempt in range(max_retries):
        response = requests.get(url)

        # Handle rate limiting
        if response.status_code == 429:
            retry_after = int(response.headers.get('Retry-After', retry_delay))
            print(f"Rate limit hit. Retrying in {retry_after} seconds...")
            time.sleep(retry_after)
            continue

        # Ensure the request is successful
        if response.status_code == 200:
            questions: List[Dict] = response.json().get('results', [])

            # Function to create a question and its related incorrect answers
            def create_question(question_dict: dict):
                new_question_id: int = q_repo.create_question(
                    Question(
                        question_text=question_dict['question'],
                        correct_answer=question_dict['correct_answer']
                    ))

                pipe(
                    question_dict['incorrect_answers'],
                    partial(map, lambda answer: ans_repo.create_answer(
                        Answer(incorrect_answer=answer), new_question_id)),
                    list
                )

            # Process the list of questions
            pipe(
                questions,
                partial(map, create_question),
                list
            )
            break
        else:
            raise Exception(f"Failed to fetch trivia questions. Status code: {response.status_code}")

    else:
        raise Exception("Max retries reached. Failed to fetch trivia questions.")


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


