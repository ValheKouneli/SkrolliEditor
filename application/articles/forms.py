from flask_wtf import FlaskForm
from wtforms import BooleanField, SelectField, StringField, validators
from application.people.models import Name
from application.auth.models import User
from application.help import getPeopleOptions


class ArticleForm(FlaskForm):
    name = StringField("Article name", [validators.Length(min=1)])
    writer = SelectField("Writer", choices=[], validators=[validators.Required()])
    ready = BooleanField("Done")

    def __init__(self, options):
        self.writer = SelectField("Writer", choices=options, validators=[validators.Required()])

    class Meta:
        csrf = False
        
