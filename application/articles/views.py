from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user

from application import app, db
from application.articles.models import Article
from application.articles.forms import ArticleForm
from application.auth.models import User
from application.help import getPeopleOptions, getEditorOptions, getIssueOptions

@app.route("/articles/", methods=["GET"])
def articles_index():
    articles = Article.get_all_articles().fetchall()
    return render_template("/articles/list.html", articles = articles)

@app.route("/articles/new/")
@login_required
def articles_form(issue=0):
    if not current_user.editor:
        return render_template("articles/list.html")

    form = ArticleForm()
    form.writer.choices = getPeopleOptions()
    form.editorInCharge.choices = getEditorOptions()
    form.issue.choices = getIssueOptions()
    form.issue.data = issue
    
    return render_template("/articles/new.html", form=form)

@app.route("/articles/<article_id>/", methods=["POST"])
@login_required

def articles_set_ready(article_id):

    #todo: give redirect address as a parameter
    a = Article.query.get(article_id)
    a.ready = True
    db.session().commit()

    return redirect(url_for("articles_index"))

@app.route("/articles/", methods=["POST"])
@login_required
def articles_create():

    if not current_user.editor:
        return render_template("articles/list.html")

    form = ArticleForm(request.form)
    form.issue.choices = getIssueOptions() # todo: keep old selection
    form.writer.choices = getPeopleOptions() # todo: keep old selection
    form.editorInCharge.choices = getEditorOptions() # todo: keep old selection

    if not form.validate():
        return render_template("articles/new.html", form = form)

    a = Article(form.name.data)
    a.issue = int(form.issue.data)
    a.writer = int(form.writer.data)
    a.editor_in_charge = int(form.editorInCharge.data)
    a.created_by = current_user.id

    db.session().add(a)
    db.session().commit()

    return redirect(url_for("articles_index"))
