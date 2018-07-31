from flask_wtf import FlaskForm
from wtforms import StringField
  
class NewPersonForm(FlaskForm):
    name = StringField("name")
  
    class Meta:
        csrf = False