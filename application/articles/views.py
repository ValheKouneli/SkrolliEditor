from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user

from application import app, db
from application.articles.models import Article
from application.articles.forms import ArticleForm
from application.auth.models import User
from application.help import getArticleWithId, getPeopleOptions, getEditorOptions, getIssueOptions

@app.route("/articles/", methods=["GET"])
def articles_index():
    articles = Article.get_all_articles().fetchall()
    return render_template("/articles/list.html", articles = articles)

@app.route("/articles/new/")
@login_required
def articles_form():
    if not current_user.editor:
        return render_template("articles/list.html")
    
    form = ArticleForm()
    form.writer.choices = getPeopleOptions()
    form.editorInCharge.choices = getEditorOptions()
    form.issue.choices = getIssueOptions()

    return render_template("/articles/new.html", form=form)

@app.route("/articles/<article_id>/", methods=["POST"])
@login_required
def articles_set_ready(article_id):

    #todo: give redirect address as a parameter
    a = Article.query.get(article_id)
    a.ready = True
    db.session().commit()

    return redirect(url_for("articles_index"))


@app.route("/article/<article_id>/", methods=["GET"])
def show_article(article_id):
    try:
        id = int(article_id)
        print("id: ", id)
    except:
        return redirect(url_for("error404"))
    article = getArticleWithId(id)
    
    if article is None:
        return redirect(url_for("error404"))

    return render_template("/articles/article.html", article=article)

@app.route("/articles/", methods=["POST"])
@login_required
def articles_create():

    if not current_user.editor:
        return render_template("articles/list.html")

    form = ArticleForm(request.form)
    form.writer.choices = getPeopleOptions()
    form.editorInCharge.choices = getEditorOptions()
    form.issue.choices = getIssueOptions()

    if not form.validate():
        return render_template("articles/new.html", form = form)

    a = Article(form.name.data)
    if form.issue.data != 0:
        a.issue = int(form.issue.data)
    if form.writer.data != 0:
        a.writer = int(form.writer.data)
    if form.editorInCharge.data != 0:
        a.editor_in_charge = int(form.editorInCharge.data)
    a.created_by = current_user.id

    db.session().add(a)
    db.session().commit()
    return redirect(url_for("articles_index"))
