from flask import render_template
from application import app
from application.help import getArticlesWithCondition
from application.articles.models import Article
from flask_login import current_user



@app.route("/")
def index():
    if current_user.is_authenticated:
        articles_writing = current_user.find_articles_writing().fetchall()
        articles_editing = current_user.find_articles_editing().fetchall()
        return render_template("index.html", logged_in=True,
            articles_writing = articles_writing,
            articles_editing = articles_editing)
    else:
        articles = getArticlesWithCondition("Article.ready = false").fetchall()
        return render_template("index.html", logged_in=False, unfinished_articles = articles)

@app.route("/404/")
def error404():
    return render_template("error404.html")
