from flask_wtf import FlaskForm
from wtforms import StringField, validators, ValidationError
from application.help import name_only_contains_certain_characters
from application.auth.models import User
import re

  
def does_not_start_with_whitespace(form, field):
    message = 'Name can not start with a whitespace character.'

    pattern = re.compile(r"^[^\\s].*$")
    if not pattern.match(field.data):
        raise ValidationError(message)
    return

def is_unique(form, field):
    message = 'Name must be unique.'

    user_with_same_name = User.query.filter_by(name=field.data).first()
    if user_with_same_name:
        raise ValidationError(message)
    return

class AliasForm(FlaskForm):
    name = StringField("Name", validators=[validators.InputRequired(),
        validators.Length(min=3, max=25), does_not_start_with_whitespace])
  
    class Meta:
        csrf = False

class NameForm(FlaskForm):
    name = StringField("Name", validators = [validators.InputRequired(), 
        validators.Length(min=1, max=25), name_only_contains_certain_characters, is_unique])

    class Meta:
        csrf = False