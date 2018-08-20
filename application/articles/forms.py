from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField, SelectField, StringField, validators
from application.people.models import Name
from application.auth.models import User

class ArticleForm(FlaskForm):
        name = StringField("Article name", [validators.Length(min=1)])
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



        
