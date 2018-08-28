from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, validators, ValidationError
from application.help import needs_a_bigger_input_field, getPeopleOptions

def isOneOfTypes(form, field):
    message = 'Choose a type.'
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
    form = set_choices(form)
    form.description.data = ""
    return form

def replicate_picture_form(form):
    replica = PictureForm(form)
    replica = set_choices(replica)
    return replica

def set_choices(form):
    choices = [(None, "(choose a type)")]
    types = map((lambda x: (x, x)), getTypes())
    for type in types:
        choices.append(type)
    form.type.choices = choices
    form.responsible.choices = getPeopleOptions()
    return form