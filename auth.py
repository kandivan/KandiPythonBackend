from functools import wraps
from flask import request, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from database import Database, User as UserModel

# Setup Flask-Login
login_manager = LoginManager()

db = Database()
session = db.get_session()

@login_manager.user_loader
def load_user(user_id):
    user_data = session.query(UserModel).filter(UserModel.id == user_id).first()
    if user_data:
        return User(user_data)

class User(UserMixin):
    def __init__(self, user_data):
        self.id = user_data.id
        self.username = user_data.name
        self.password = user_data.password

def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth = request.authorization
        if not auth or not auth.username or not auth.password:
            return jsonify({'message': 'Missing username or password'}), 401

        user_data = session.query(UserModel).filter(UserModel.name == auth.username).first()
        user = User(user_data) if user_data else None
        if user and check_password_hash(user.password, auth.password):
            login_user(user)
            return func(*args, **kwargs)
        else:
            return jsonify({'message': 'Invalid credentials'}), 401

    return wrapper

@login_required
def authorize(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Authorization logic: You can add additional checks here
        return func(*args, **kwargs)
    return wrapper
