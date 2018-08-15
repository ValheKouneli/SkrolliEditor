from flask_wtf import FlaskForm
from wtforms import IntegerField
  
class TestForm(FlaskForm):
    slider = IntegerField("Name")
  
    class Meta:
        csrf = False