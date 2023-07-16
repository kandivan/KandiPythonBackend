from functools import wraps
from flask import request, jsonify
from flask_wtf import FlaskForm
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from wtforms  import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError, Email
from werkzeug.security import check_password_hash, generate_password_hash
from database import Database, User

# Setup Flask-Login
login_manager = LoginManager()
db = Database()
session = db.get_session()

@login_manager.user_loader
def load_user(user_id):
    return session.query(User).get(user_id)

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)],
                            render_kw={"placeholder": "Username"})
    email = StringField('Email', validators=[InputRequired(), Email()],
                         render_kw={"placeholder": "Email"})
    password = PasswordField('Password', validators=[InputRequired(), Length(min=4, max=20)],
                              render_kw={"placeholder": "Password"})
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        existing_user_username = session.query(User).filter_by(username=username.data.lower()).first()
        if existing_user_username:
            raise ValidationError("That username already exists. Please choose a different one.")

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)],
                            render_kw={"placeholder": "Username"})
    password = PasswordField('Password', validators=[InputRequired(), Length(min=4, max=20)],
                              render_kw={"placeholder": "Password"})
    submit = SubmitField('Login')

def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth = request.authorization
        if not auth or not auth.username or not auth.password:
            return jsonify({'message': 'Missing username or password'}), 401

        user_data = session.query(User).filter(User.Username == auth.username).first()
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
