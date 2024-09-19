import pytest

from service.service import user_with_highest_score
from model.User import User
from repository.database import create_tables
import repository.user_answer_repository as u_a_repos


@pytest.fixture(scope="module")
def setup_database():
    create_tables()


def test_get_user_answers(setup_database):
    user_answers = u_a_repos.get_user_answers()
    assert len(user_answers) > 0

def test_user_with_highest_score(setup_database):
    highest_score_user = user_with_highest_score()
    assert isinstance(highest_score_user, User)
    assert isinstance(highest_score_user.first, str)