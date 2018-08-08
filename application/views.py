from flask import render_template
from application import app
from application.help import getArticlesWithCondition
from application.articles.models import Article
from flask_login import current_user

@app.route("/")
def index():
    if current_user.is_authenticated:
        return render_template("index.html", logged_in=True,
            articles_writing = current_user.find_articles_writing(),
            articles_editing = current_user.find_articles_editing())
    else:
        articles = getArticlesWithCondition("Article.ready = 0")
        return render_template("index.html", logged_in=False, unfinished_articles = articles)