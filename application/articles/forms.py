from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField

class ArticleForm(FlaskForm):
    name = StringField("Article name")
    ready = BooleanField("Done")

    class Meta:
        csrf = False