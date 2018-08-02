from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators, ValidationError
import re
  
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

class RegisterForm(FlaskForm):
    username = StringField("Username", [validators.Length(min=5)])
    name = StringField("Name", [validators.Length(min=1)])
    password = PasswordField("Password", [validators.InputRequired(), password_strength_check])
    confirm = PasswordField("Confirm password", [validators.EqualTo('password', message="Passwords must match.")])

    class Meta:
        csrf = False