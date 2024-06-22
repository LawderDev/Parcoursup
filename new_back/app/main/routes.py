from flask import Blueprint, jsonify, request
from . import main
from ..controllers.user_controller import get_user_by_id, create_user

@main.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = get_user_by_id(user_id)
    if user:
        return jsonify({'id': user.id, 'username': user.username, 'email': user.email})
    return jsonify({'error': 'User not found'}), 404

@main.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    new_user = create_user(data['username'], data['email'])
    return jsonify({'id': new_user.id, 'username': new_user.username, 'email': new_user.email}), 201