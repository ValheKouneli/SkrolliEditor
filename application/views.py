from flask import render_template
from application import app
from application.articles.models import Article
from flask_login import current_user

@app.route("/")
def index():
    if current_user.is_authenticated:
        return render_template("index.html", logged_in=True, articles_writing = current_user.find_articles_writing())
    else:
        articles = Article.find_articles_not_ready()
        return render_template("index.html", logged_in=False, unfinished_articles = articles)