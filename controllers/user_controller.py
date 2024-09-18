from dataclasses import asdict

from flask import request
from flask import Blueprint, jsonify

import repository.user_repository as u_repo
from model.User import User

user_blueprint = Blueprint("users", __name__)

@user_blueprint.route('/', methods=['GET'])
def get_all_users():
    users = list(map(asdict, u_repo.get_all_users()))
    return jsonify(users), 200

@user_blueprint.route('/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id: int):
    user = u_repo.get_by_id(user_id)
    return jsonify(asdict(user)) , 200

@user_blueprint.route('/create', methods=['POST'])
def create_user():
    json = request.json
    new_user: dict = {**json}
    new_id: int = u_repo.create_user(User.from_dict(new_user))
    created_user: User = u_repo.get_by_id(new_id)
    return jsonify(created_user), 201

@user_blueprint.route('/users/delete/<int:user_id>', methods=['DELETE'])
def delete_user(user_id: int):
    u_repo.delete_user(user_id)
    return jsonify({'message': f'user by id: {user_id} deleted successfully'}), 200

@user_blueprint.route('/users/update/<int:user_id>', methods=['PUT'])
def update_user(user_id: int):
    json = request.json
    user = User.from_dict({**json})
    u_repo.update_user(user, user_id)
    updated_user: User = u_repo.get_by_id(user_id)
    return jsonify(updated_user), 200