from flask import redirect, render_template, request, url_for

from application import app, db
from application.articles.models import Article
from application.articles.forms import ArticleForm

@app.route("/articles/", methods=["GET"])
def articles_index():
    return render_template("/articles/list.html", articles = Article.query.all())

@app.route("/articles/new/")
def articles_form():
    return render_template("/articles/new.html", form = ArticleForm())

@app.route("/articles/<article_id>/", methods=["POST"])
def articles_set_ready(article_id):

    a = Article.query.get(article_id)
    a.ready = True
    db.session().commit()

    return redirect(url_for("articles_index"))

@app.route("/articles/", methods=["POST"])
def articles_create():
    form = ArticleForm(request.form)

    if not form.validate():
        return render_template("articles/new.html", form = form)

    a = Article(form.name.data)
    a.writer = form.writer.data

    db.session().add(a)
    db.session().commit()

    return redirect(url_for("articles_index"))
