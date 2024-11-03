from flask import Blueprint, request, jsonify
from flask_login import login_required, login_user, logout_user
from user_dao import UserDao
import bcrypt

user_blueprint = Blueprint('user_blueprint', __name__)
user_dao = UserDao('climbing_management.db')


@user_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = user_dao.get_user_by_username(data['username'])
    if user and bcrypt.checkpw(data['password'].encode('utf-8'), user.password):
        login_user(user)
        return jsonify({'success': True}), 200
    return jsonify({'error': 'Invalid username or password'}), 401


@user_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'success': True}), 200
