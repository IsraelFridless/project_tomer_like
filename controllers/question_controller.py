from dataclasses import asdict
from typing import List

from flask import request
from flask import Blueprint, jsonify
from toolz import pipe
from toolz.curried import partial

import repository.question_repository as q_repo
import repository.answer_repository as ans_repo
from model.Answer import Answer
from model.Question import Question

question_blueprint = Blueprint("questions", __name__)

@question_blueprint.route('/', methods=['GET'])
def get_all_questions():
    questions = list(map(asdict, q_repo.get_all_questions()))
    return jsonify(questions), 200

@question_blueprint.route('/users/<int:question_id>', methods=['GET'])
def get_question_by_id(user_id: int):
    user = q_repo.get_by_id(user_id)
    return jsonify(asdict(user)) , 200

@question_blueprint.route('/create', methods=['POST'])
def create_question():
    json = request.json
    unpacked: dict = {**json}
    new_question_id: int = q_repo.create_question(
        Question(
        question_text=unpacked['question_text'],
        correct_answer=unpacked['correct_answer']
    ))
    created_question: Question = q_repo.get_by_id(new_question_id)
    incorrect_answers: List[Answer] = pipe(
        unpacked['incorrect_answers'],
        partial(map, lambda answer: ans_repo.create_answer(Answer(question_id=new_question_id, incorrect_answer=answer))),
        partial(map, lambda answer_id: ans_repo.get_by_id(answer_id)),
        list
    )
    return jsonify({'created_question': created_question, 'incorrect_answers': incorrect_answers}), 201

@question_blueprint.route('/users/delete/<int:question_id>', methods=['DELETE'])
def delete_question(question_id: int):
    q_repo.delete_question(question_id)
    return jsonify({'message': f'question by id: {question_id} deleted successfully'}), 200

@question_blueprint.route('/users/update/<int:question_id>', methods=['PUT'])
def update_question(question_id: int):
    json = request.json
    question = Question.from_dict({**json})
    q_repo.update_question(question, question_id)
    updated_question: Question = q_repo.get_by_id(question_id)
    return jsonify(updated_question), 200