from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField, SelectField, StringField, validators, ValidationError

from application.help import getPeopleOptions, getEditorOptions, \
    getIssueOptions, needs_a_bigger_input_field

import re

def is_a_proper_name(form, field):
    message = 'Article name has to start with a capital letter or a number.'

    pattern = re.compile(r"^[1-9A-ZÖÄÅ].*$")
    if not pattern.match(field.data):
        raise ValidationError(message)
    return

class ArticleForm(FlaskForm):
        name = StringField("Article name", validators=[validators.InputRequired(),
            validators.Length(min=1, max=30), is_a_proper_name])
        issue = SelectField("Issue", coerce=int)
        writer = SelectField("Writer", coerce=int)
        editorInCharge = SelectField("Editor-in-charge", coerce=int)
        synopsis = StringField("Synopsis", validators=[needs_a_bigger_input_field()])


        class Meta:
            csrf = False

def create_article_form():
    form = ArticleForm()
    form = set_options(form)
    return form

def replicate_article_form(form):
    replica = ArticleForm(form)
    replica = set_options(replica)
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
        
