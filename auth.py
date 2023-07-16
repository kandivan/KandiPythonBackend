from flask_wtf import FlaskForm
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from wtforms  import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError, Email
from database import Database, User

# Setup Flask-Login
login_manager = LoginManager()
db = Database()
session = db.get_session()

@login_manager.user_loader
def load_user(user_id):
    return session.query(User).get(user_id)

def get_user(username):
    return session.query(User).filter_by(username=username).first()

def register_user(username: str, email: str, hashed_password: str):
    new_user = User(username=username, email=email, password=hashed_password)
    session.add(new_user)
    session.commit()

def change_password(bcrypt: Bcrypt, user: User, old_password: str, new_password: str):
    if user.check_password(bcrypt, old_password):
        user.set_password(bcrypt, new_password)
        session.commit()
        return True
    else:
        raise ValidationError("Incorrect password.")

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[InputRequired()])
    new_password = PasswordField('New Password', validators=[InputRequired(), Length(min=4, max=20)])
    submit = SubmitField('Change Password')

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


