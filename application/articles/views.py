from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user

from application import app, db
from application.articles.models import Article
from application.articles.forms import ArticleForm, getPeopleOptions
from application.auth.models import User

@app.route("/articles/", methods=["GET"])
def articles_index():
    data = Article.query.all()
    articles = [{'name': article.name, 'writer': User.query.get(article.writer).name, 'ready': article.ready} for article in data]
    return render_template("/articles/list.html", articles = articles)

@app.route("/articles/new/")
@login_required
def articles_form():
    if not current_user.editor:
        return render_template("articles/list.html")
    
    form = ArticleForm()
    form.writer.choices = getPeopleOptions()

    return render_template("/articles/new.html", form = form)

@app.route("/articles/<article_id>/", methods=["POST"])
@login_required

def articles_set_ready(article_id):

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
    form.writer.choices = getPeopleOptions()

    if not form.validate():
        return render_template("articles/new.html", form = form)

    a = Article(form.name.data)
    a.writer = int(form.writer.data)
    a.created_by = current_user.id

    db.session().add(a)
    db.session().commit()

    return redirect(url_for("articles_index"))
