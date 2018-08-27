from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, validators
from application.help import needs_a_bigger_input_field

class PictureForm(FlaskForm):
    description = StringField("Description",
        validators = [
            validators.InputRequired(),
            validators.Length(min=10, max=200),
            needs_a_bigger_input_field()
            ])
    responsible = SelectField("Responsible", coerce=int)

    class Meta:
        csrf = False