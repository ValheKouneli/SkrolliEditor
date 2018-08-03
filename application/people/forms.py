from flask_wtf import FlaskForm
from wtforms import StringField, validators
  
class NameForm(FlaskForm):
    name = StringField("Name", [validators.Length(min=3)])
  
    class Meta:
        csrf = False