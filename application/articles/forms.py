from flask_wtf import FlaskForm
from wtforms import BooleanField, SelectField, StringField, validators
from application.people.models import Name
from application.auth.models import User

class ArticleForm(FlaskForm):
        name = StringField("Article name", [validators.Length(min=1)])
        issue = SelectField("Issue", coerce=int)
        writer = SelectField("Writer", coerce=int)
        editorInCharge = SelectField("Editor-in-charge", coerce=int)
        ready = BooleanField("Done")


        class Meta:
            csrf = False



        
