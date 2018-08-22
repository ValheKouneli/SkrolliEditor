from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField, SelectField, StringField, validators, ValidationError
from application.people.models import Name
from application.auth.models import User

import re

def is_a_proper_name(form, field):
    message = 'Article name has to start with a capital letter or a number.'

    pattern = re.compile(r"^[1-9A-ZÖÄÅ].*$")
    if not pattern.match(field.data):
        raise ValidationError(message)
    return

class ArticleForm(FlaskForm):
        name = StringField("Article name", validators=[validators.Length(min=1, max=20),
            is_a_proper_name])
        issue = SelectField("Issue", coerce=int)
        writer = SelectField("Writer", coerce=int)
        editorInCharge = SelectField("Editor-in-charge", coerce=int)
        synopsis = StringField("Synopsis")


        class Meta:
            csrf = False

class StatusForm(FlaskForm):
        article_id = IntegerField("Article id")
        writing_status = IntegerField("Writing status")
        editing_status = IntegerField("Editing status")

        class Meta:
            csrf = False



        
