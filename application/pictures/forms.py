from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, validators, ValidationError
from application.help import needs_a_bigger_input_field, getPeopleOptions

def isOneOfTypes(form, field):
    message = 'Type must be one of the approved types.'
    types = getTypes()
    if not field.data in types:
        raise ValidationError(message)
    return

def getTypes():
    types = [
        "Opening picture",
        "Photograph",
        "Graph",
        "Illustration",
        "Other"]
    return types

class PictureForm(FlaskForm):
    type = SelectField("Type",
        validators=[isOneOfTypes, validators.InputRequired()], coerce=str)
    description = StringField("Description",
        validators = [
            validators.InputRequired(),
            validators.Length(min=10, max=200),
            needs_a_bigger_input_field()
            ])
    responsible = SelectField("Responsible", coerce=int)

    class Meta:
        csrf = False

def create_picture_form():
    form = PictureForm()
    form.type.choices = map((lambda x: (x, x)), getTypes())
    form.responsible.choices = getPeopleOptions()
    return form

def replicate_picture_form(form):
    replica = PictureForm(form)
    replica.type.choices = map((lambda x: (x, x)), getTypes())
    replica.responsible.choices = getPeopleOptions()
    return replica