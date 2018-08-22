from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators, ValidationError
import re

from application.auth.models import User
from application.help import name_only_contains_certain_characters
  
class LoginForm(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")

    class Meta:
        csrf = False

def password_strength_check(form, field):
    if len(field.data) > 50:
        raise ValidationError('Password must be less than 50 characters.')
    if len(field.data) < 8:
        raise ValidationError('Password must be at least 8 characters.')
    # if not bool(re.search('[a-zA-Z]', field.data)) or \
    #     not bool(re.search('[0-9]', field.data)) or \
    #     not bool(re.search('[!@#$%^&*()_+\\-=\\[\\]\\{\\};\':\"\\\\|,.<>\\/?]', field.data)):
    #     raise ValidationError('Password must contain letters, numbers and special characters.')

def new_password_strength_check(form, field):
    if len(field.data) > 0:
        password_strength_check(form, field)

def username_uniqueness_check(form, field):
    user_by_same_name = User.query.filter_by(username = field.data).first()
    # todo: make it case-insensitive
    
    if user_by_same_name is None:
        return
    else:
        raise ValidationError('Account is taken.')

def username_only_alphanumerics_check(form, field):
    message = 'Username can contain only numbers and letters.'

    pattern = re.compile(r"^[1-9A-Za-z]*$")
    if not pattern.match(field.data):
        raise ValidationError(message)
    return 

class RegisterForm(FlaskForm):
    username = StringField("Username", validators = [validators.InputRequired, 
        username_uniqueness_check, username_only_alphanumerics_check,
        validators.Length(min=4, max=10)])
    name = StringField("Name", validators = [validators.InputRequired(), 
        validators.Length(min=1, max=25), name_only_contains_certain_characters])
    password = PasswordField("Password", validators = [validators.InputRequired(),
        validators.Length(min=8, max=144), password_strength_check])
    confirm = PasswordField("Confirm password", validators=[validators.InputRequired(),
        validators.EqualTo('password', message="Passwords must match.")])

    class Meta:
        csrf = False

class UpdateAccountForm(FlaskForm):
    name = StringField("Name", validators=[validators.Length(min=1, max=25),
        name_only_contains_certain_characters])
    password = PasswordField("New password", validators = [new_password_strength_check,
        validators.Length(max=144)])
    confirm = PasswordField("Confirm password", [validators.EqualTo('password', message="Passwords must match.")])
    oldpassword = PasswordField("Password", [validators.InputRequired()])

    class Meta:
        csrf = False