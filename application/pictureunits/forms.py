from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, validators

class IssueForm(FlaskForm):
    name = StringField("Description",
        validators = [validators.InputRequired(), validators.Length(min=10, max=200)])
    responsible = SelectField("Responsible", coerce=int)

    class Meta:
        csrf = False