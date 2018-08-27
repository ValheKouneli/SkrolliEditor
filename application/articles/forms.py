from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField, SelectField, StringField, validators, ValidationError
from application.people.models import Name
from application.auth.models import User
from application.help import needs_a_bigger_input_field

import re

def is_a_proper_name(form, field):
    message = 'Article name has to start with a capital letter or a number.'

    pattern = re.compile(r"^[1-9A-ZÖÄÅ].*$")
    if not pattern.match(field.data):
        raise ValidationError(message)
    return

class ArticleForm(FlaskForm):
        name = StringField("Article name", validators=[validators.InputRequired(),
            validators.Length(min=1, max=30), is_a_proper_name])
        issue = SelectField("Issue", coerce=int)
        writer = SelectField("Writer", coerce=int)
        editorInCharge = SelectField("Editor-in-charge", coerce=int)
        synopsis = StringField("Synopsis", validators=[needs_a_bigger_input_field()])


        class Meta:
            csrf = False
        
