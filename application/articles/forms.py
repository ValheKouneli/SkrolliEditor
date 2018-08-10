from flask_wtf import FlaskForm
from wtforms import BooleanField, SelectField, StringField, validators
from application.people.models import Name
from application.auth.models import User

from operator import itemgetter

def getPeopleOptions():
    choices = []
    names = Name.query.all()
    for name in names:
        user = User.query.filter_by(id = name.user_id).first()
        choices.append((str(name.user_id), name.name + ' (' + user.name + ')'))
    print("choises: ", choices)
    return sorted(choices, key=lambda choice: choice[0], reverse=True)

class ArticleForm(FlaskForm):
    name = StringField("Article name", [validators.Length(min=1)])
    writer = SelectField("Writer", validators=[validators.Required()])
    ready = BooleanField("Done")

    class Meta:
        csrf = False

