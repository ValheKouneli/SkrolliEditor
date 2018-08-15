from flask_wtf import FlaskForm
from wtforms import StringField, validators, ValidationError
from application.issues.models import Issue
from application.auth.models import User

import re

def is_unique(form, field):
    message = 'Issue name must be unique.'

    issue_with_same_name = Issue.query.filter_by(name=field.data).first()
    if issue_with_same_name:
        raise ValidationError(message)
    return

def is_correct_format(form, field):
    message = 'Issue name is in the wrong format.'

    pattern = re.compile(r"^[1-9][0-9]{3}\.[1-4]E?$")
    if not pattern.match(field.data):
        raise ValidationError(message)
    return

class IssueForm(FlaskForm):
    name = StringField("Issue number",
        validators = [validators.Length(min=5), is_unique, is_correct_format])

    class Meta:
        csrf = False