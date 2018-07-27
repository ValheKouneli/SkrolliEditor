from application import app, db
from flask import redirect, render_template, request, url_for
from application.articles.models import Article

@app.route("/articles/", methods=["GET"])
def articles_index():
    return render_template("/articles/list.html", articles = Article.query.all())

@app.route("/articles/new/")
def articles_form():
    return render_template("/articles/new.html")

@app.route("/articles/<article_id>/", methods=["POST"])
def articles_set_ready(article_id):

    a = Article.query.get(article_id)
    a.ready = True
    db.session().commit()

    return redirect(url_for("articles_index"))

@app.route("/articles/", methods=["POST"])
def articles_create():
    a = Article(request.form.get("name"))

    db.session().add(a)
    db.session().commit()

    return redirect(url_for("articles_index"))
