from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, validators

class ArticleForm(FlaskForm):
    name = StringField("Article name", [validators.Length(min=1)])
    writer = StringField("Writer", [validators.Length(min=1)])
    ready = BooleanField("Done")

    class Meta:
        csrf = False