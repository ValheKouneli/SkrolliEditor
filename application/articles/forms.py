from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField, SelectField, StringField, validators, ValidationError

from application.help import getPeopleOptions, \
    getIssueOptions, needs_a_bigger_input_field
from application.auth.models import getEditorOptions

import re

def is_a_proper_name(form, field):
    message = 'Article name has to start with a capital letter or a number.'

    pattern = re.compile(r"^[1-9A-ZÖÄÅ].*$")
    if not pattern.match(field.data):
        raise ValidationError(message)
    return

def is_not_same_as_writer(form, field):
    message = "Editor-in-charge can not be the same as the writer."

    if field.data != 0 and field.data == form.writer.data:
        raise ValidationError(message)
    return

class ArticleForm(FlaskForm):
        name = StringField("Article name", validators=[validators.InputRequired(),
            validators.Length(min=1, max=30), is_a_proper_name])
        issue = SelectField("Issue", coerce=int)
        writer = SelectField("Writer", coerce=int)
        editorInCharge = SelectField("Editor-in-charge",
            validators=[is_not_same_as_writer],
            coerce=int)
        beginningPicture = BooleanField("Beginning picture", default="checked")
        illustration = BooleanField("Illustrations", default="checked")
        photograph = BooleanField("Photograph", default="checked")
        graph = BooleanField("Graph", default="checked")
        screencap = BooleanField("Screencaps", default="checked")
        synopsis = StringField("Synopsis", validators=[needs_a_bigger_input_field()])


        class Meta:
            csrf = False

def create_article_form():
    form = ArticleForm()
    form = set_options(form)
    form.synopsis.data = ""
    return form

def replicate_article_form(form):
    replica = ArticleForm(form)
    replica = set_options(replica)
    if not replica.synopsis.data:
        replica.synopsis.data = ""
    return replica

def set_options(articleform):
    articleform.writer.choices = getPeopleOptions()
    articleform.editorInCharge.choices = getEditorOptions()
    articleform.issue.choices = getIssueOptions()
    return articleform

def set_article_according_to_form(article, form):
    article.set_name(form.name.data)
    article.set_writer(int(form.writer.data))
    article.set_issue(int(form.issue.data))
    article.set_editor(int(form.editorInCharge.data))
    return article
        
