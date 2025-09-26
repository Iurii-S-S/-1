from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from . import db
from .models import User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password are required'}), 400
    
    user = User.query.filter_by(email=data['email']).first()
    
    if user and user.check_password(data['password']):
        login_user(user)
        return jsonify({
            'message': 'Login successful',
            'user': user.to_dict()
        })
    
    return jsonify({'error': 'Invalid credentials'}), 401

@auth.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logout successful'})

@auth.route('/profile', methods=['GET'])
@login_required
def profile():
    return jsonify(current_user.to_dict())

@auth.route('/users', methods=['GET'])
@login_required
def get_users():
    if current_user.role != 'manager':
        return jsonify({'error': 'Access denied'}), 403
    
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])