from itertools import groupby

from toolz import pipe
from toolz.curried import partial

import repository.user_answer_repository as u_a_repos
import repository.user_repository as u_repos
import repository.question_repository as q_repos
from model.User import User


# Exercise 1
# Description: Find the user with the highest score (most correctly answered questions)

def user_with_highest_score() -> User:
    users = u_repos.get_all_users()
    answers = u_a_repos.get_user_answers()

    grouped_answers = {k: list(v) for k, v in groupby(answers, key=lambda ua: ua.user_id)}

    highest_score_user = max(
        users,
        key=lambda user: len([ua for ua in grouped_answers.get(user.id, []) if ua.is_correct])
    )

    return highest_score_user




# Exercise 2
# Description: Find the question that was answered correctly the fastest


# Exercise 3
# Description: Find the second-place user and their fastest answer time


# Exercise 4
# Description: Calculate the average time taken to answer each question


# Exercise 5
# Description: Calculate the success rate for each question


# Exercise 6
# Description: Find users who have answered all questions


# Exercise 7
# Description: Calculate the median time taken for correct answers vs incorrect answers


# Exercise 8
# Description: Generate a comprehensive report for each user
# containing total_questions, answered_questions
# , correct_answers, avg_time, fastest_answer, slowest_answer
# , unanswered_questions. Export result to csv.
