from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField

class ArticleForm(FlaskForm):
    name = StringField("Article name")
    writer = StringField("Writer")
    ready = BooleanField("Done")

    class Meta:
        csrf = False