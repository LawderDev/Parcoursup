from flask import Blueprint, jsonify, request
from . import main
from app.controllers import user_controller, group_controller, session_controller, project_controller, group_preferencies_controller, project_preferencies_controller, student_controller

@main.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = user_controller.get_user_by_id(user_id)
    if user:
        return jsonify({'id': user.id, 'username': user.username, 'email': user.email})
    return jsonify({'error': 'User not found'}), 404

@main.route('/hello', methods=['GET'])
def hello():
    return "Hello World"

@main.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    new_user = user_controller.create_user(data['username'], data['email'])
    return jsonify({'id': new_user.id, 'username': new_user.username, 'email': new_user.email}), 201